/*
 * Complete DPLL solver and tree-like DRUP proof producer for the 64-variable
 * z(20) fixed-core CNFs.  It deliberately uses no clause learning: each
 * conflicting decision cube yields its blocking clause by RUP, and the two
 * child blocking clauses yield the parent blocking clause by RUP.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct { uint64_t positive, negative, variables; } Clause;

static Clause *clauses;
static int number_of_clauses, number_of_variables;
static FILE *proof_file;
static int decision_path[64];
static unsigned long long nodes, decisions, propagations, conflicts, proof_lines;

static void emit_blocking_clause(int depth) {
    for (int i = 0; i < depth; ++i) fprintf(proof_file, "%d ", -decision_path[i]);
    fprintf(proof_file, "0\n");
    ++proof_lines;
}

static int unit_propagate(uint64_t *true_variables, uint64_t *false_variables) {
    uint64_t assigned = *true_variables | *false_variables;
    int changed = 1;
    while (changed) {
        changed = 0;
        for (int i = 0; i < number_of_clauses; ++i) {
            Clause clause = clauses[i];
            if ((clause.positive & *true_variables) ||
                (clause.negative & *false_variables)) continue;
            uint64_t remaining = clause.variables & ~assigned;
            if (!remaining) {
                ++conflicts;
                return 0;
            }
            if ((remaining & (remaining - 1)) == 0) {
                if (clause.positive & remaining) *true_variables |= remaining;
                else *false_variables |= remaining;
                assigned |= remaining;
                ++propagations;
                changed = 1;
            }
        }
    }
    return 1;
}

static int choose_variable(uint64_t true_variables, uint64_t false_variables,
                           int *prefer_true) {
    uint64_t assigned = true_variables | false_variables;
    int minimum_length = 100;
    int positive_score[64] = {0};
    int negative_score[64] = {0};

    for (int i = 0; i < number_of_clauses; ++i) {
        Clause clause = clauses[i];
        if ((clause.positive & true_variables) ||
            (clause.negative & false_variables)) continue;
        uint64_t remaining = clause.variables & ~assigned;
        int length = __builtin_popcountll(remaining);
        if (length < minimum_length) {
            minimum_length = length;
            memset(positive_score, 0, sizeof positive_score);
            memset(negative_score, 0, sizeof negative_score);
        }
        if (length == minimum_length) {
            for (uint64_t bits = remaining; bits; bits &= bits - 1) {
                int variable = __builtin_ctzll(bits);
                uint64_t bit = UINT64_C(1) << variable;
                if (clause.positive & bit) ++positive_score[variable];
                else ++negative_score[variable];
            }
        }
    }

    int best_variable = -1;
    int best_score = -1;
    for (int variable = 0; variable < number_of_variables; ++variable) {
        if (assigned & (UINT64_C(1) << variable)) continue;
        int score = (positive_score[variable] + 1) *
                    (negative_score[variable] + 1);
        if (score > best_score) {
            best_score = score;
            best_variable = variable;
        }
    }
    if (best_variable >= 0)
        *prefer_true = positive_score[best_variable] >= negative_score[best_variable];
    return best_variable;
}

static int solve(uint64_t true_variables, uint64_t false_variables, int depth) {
    ++nodes;
    if (!unit_propagate(&true_variables, &false_variables)) {
        emit_blocking_clause(depth);
        return 0;
    }
    if (__builtin_popcountll(true_variables | false_variables) == number_of_variables)
        return 1;

    int prefer_true = 1;
    int variable = choose_variable(true_variables, false_variables, &prefer_true);
    if (variable < 0) return 1;
    ++decisions;
    uint64_t bit = UINT64_C(1) << variable;
    int preferred_literal = prefer_true ? variable + 1 : -(variable + 1);

    decision_path[depth] = preferred_literal;
    if (prefer_true ? solve(true_variables | bit, false_variables, depth + 1)
                    : solve(true_variables, false_variables | bit, depth + 1))
        return 1;

    decision_path[depth] = -preferred_literal;
    if (prefer_true ? solve(true_variables, false_variables | bit, depth + 1)
                    : solve(true_variables | bit, false_variables, depth + 1))
        return 1;

    /* Child clauses are (not path OR not x) and (not path OR x).  Under the
       parent path they unit-propagate to a conflict, so (not path) is RUP. */
    emit_blocking_clause(depth);
    return 0;
}

static void read_dimacs(const char *path) {
    FILE *input = fopen(path, "r");
    if (!input) { perror(path); exit(2); }
    char line[4096];
    do {
        if (!fgets(line, sizeof line, input)) { fprintf(stderr, "bad DIMACS\n"); exit(2); }
    } while (line[0] == 'c' || line[0] == '\n');
    if (sscanf(line, "p cnf %d %d", &number_of_variables, &number_of_clauses) != 2 ||
        number_of_variables > 64) {
        fprintf(stderr, "bad DIMACS header\n");
        exit(2);
    }
    clauses = calloc((size_t)number_of_clauses, sizeof *clauses);
    if (!clauses) { perror("calloc"); exit(2); }

    int clause_index = 0, literal;
    while (clause_index < number_of_clauses && fscanf(input, "%d", &literal) == 1) {
        if (!literal) {
            clauses[clause_index].variables =
                clauses[clause_index].positive | clauses[clause_index].negative;
            ++clause_index;
        } else {
            int variable = abs(literal) - 1;
            uint64_t bit = UINT64_C(1) << variable;
            if (literal > 0) clauses[clause_index].positive |= bit;
            else clauses[clause_index].negative |= bit;
        }
    }
    fclose(input);
    if (clause_index != number_of_clauses) {
        fprintf(stderr, "read %d of %d clauses\n", clause_index, number_of_clauses);
        exit(2);
    }
}

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s input.cnf output.drup\n", argv[0]);
        return 2;
    }
    read_dimacs(argv[1]);
    proof_file = fopen(argv[2], "w");
    if (!proof_file) { perror(argv[2]); return 2; }
    clock_t start = clock();
    int satisfiable = solve(0, 0, 0);
    double seconds = (double)(clock() - start) / CLOCKS_PER_SEC;
    fclose(proof_file);
    fprintf(stderr,
            "s %s nodes=%llu decisions=%llu propagations=%llu conflicts=%llu "
            "proof_lines=%llu cpu_seconds=%.3f\n",
            satisfiable ? "SAT" : "UNSAT", nodes, decisions, propagations,
            conflicts, proof_lines, seconds);
    return satisfiable ? 10 : 20;
}
