/* Independent forward checker for the RUP subset of DRAT used here. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct { uint64_t positive, negative, variables; } Clause;
static Clause *database;
static size_t database_size, database_capacity;
static int number_of_variables;

static void append_clause(Clause clause) {
    if (database_size == database_capacity) {
        database_capacity = database_capacity ? 2 * database_capacity : 131072;
        database = realloc(database, database_capacity * sizeof *database);
        if (!database) { perror("realloc"); exit(2); }
    }
    database[database_size++] = clause;
}

static void read_dimacs(const char *path) {
    FILE *input = fopen(path, "r");
    if (!input) { perror(path); exit(2); }
    char line[4096];
    int declared_clauses = -1;
    while (fgets(line, sizeof line, input)) {
        if (line[0] == 'c' || line[0] == '\n') continue;
        if (line[0] == 'p') {
            if (sscanf(line, "p cnf %d %d", &number_of_variables,
                       &declared_clauses) != 2 || number_of_variables > 64) {
                fprintf(stderr, "bad DIMACS header\n");
                exit(2);
            }
            break;
        }
    }
    Clause clause = {0};
    int literal, clauses_read = 0;
    while (fscanf(input, "%d", &literal) == 1) {
        if (!literal) {
            clause.variables = clause.positive | clause.negative;
            append_clause(clause);
            clause = (Clause){0};
            ++clauses_read;
        } else {
            int variable = abs(literal) - 1;
            uint64_t bit = UINT64_C(1) << variable;
            if (literal > 0) clause.positive |= bit;
            else clause.negative |= bit;
        }
    }
    fclose(input);
    if (clauses_read != declared_clauses) {
        fprintf(stderr, "read %d of %d clauses\n", clauses_read, declared_clauses);
        exit(2);
    }
}

static int reverse_unit_propagates(Clause target) {
    /* Falsifying target sets its negative literals true and positives false. */
    uint64_t true_variables = target.negative;
    uint64_t false_variables = target.positive;
    if (true_variables & false_variables) return 1;
    uint64_t assigned = true_variables | false_variables;

    int changed = 1;
    while (changed) {
        changed = 0;
        for (size_t i = 0; i < database_size; ++i) {
            Clause clause = database[i];
            if ((clause.positive & true_variables) ||
                (clause.negative & false_variables)) continue;
            uint64_t remaining = clause.variables & ~assigned;
            if (!remaining) return 1;
            if ((remaining & (remaining - 1)) == 0) {
                if (clause.positive & remaining) true_variables |= remaining;
                else false_variables |= remaining;
                assigned |= remaining;
                changed = 1;
            }
        }
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s input.cnf proof.drup\n", argv[0]);
        return 2;
    }
    read_dimacs(argv[1]);
    size_t original_size = database_size;
    FILE *proof = fopen(argv[2], "r");
    if (!proof) { perror(argv[2]); return 2; }

    Clause clause = {0};
    int literal, saw_empty_clause = 0;
    size_t proof_line = 0;
    clock_t start = clock();
    while (fscanf(proof, "%d", &literal) == 1) {
        if (!literal) {
            clause.variables = clause.positive | clause.negative;
            ++proof_line;
            if (!reverse_unit_propagates(clause)) {
                fprintf(stderr, "RUP failure at proof line %zu\n", proof_line);
                return 1;
            }
            if (!clause.variables) saw_empty_clause = 1;
            append_clause(clause);
            clause = (Clause){0};
        } else {
            int variable = abs(literal) - 1;
            if (variable < 0 || variable >= number_of_variables) {
                fprintf(stderr, "bad proof literal %d\n", literal);
                return 2;
            }
            uint64_t bit = UINT64_C(1) << variable;
            if (literal > 0) clause.positive |= bit;
            else clause.negative |= bit;
        }
    }
    fclose(proof);
    if (!saw_empty_clause) {
        fprintf(stderr, "proof contains no empty clause\n");
        return 1;
    }
    double seconds = (double)(clock() - start) / CLOCKS_PER_SEC;
    fprintf(stderr,
            "VERIFIED original_clauses=%zu proof_lines=%zu total_clauses=%zu "
            "cpu_seconds=%.3f\n",
            original_size, proof_line, database_size, seconds);
    return 0;
}
