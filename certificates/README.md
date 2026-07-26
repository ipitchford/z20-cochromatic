# Candidate certificate package for `z(20)=6`

This package reduces the 20-vertex cochromatic problem to two 64-variable SAT instances and supplies a text DRUP proof of UNSAT for each instance.

## Mathematical reduction

1. Every graph on 20 vertices contains a homogeneous 4-set because `R(4,4)=18`.
2. A graph containing two vertex-disjoint homogeneous 4-sets is 6-cocolourable: use those two sets as classes, and partition the remaining 12 vertices into at most four homogeneous classes using the known value `z(12)=4`.
3. Therefore a counterexample to `z(20)=6` would have no two disjoint homogeneous 4-sets. Fix one homogeneous 4-set `A`; complement the graph if necessary so that `A` is a clique. The induced graph on the remaining 16 vertices must contain no clique or independent set of order four.
4. Brendan McKay's complete Ramsey catalogue contains exactly two Ramsey(4,4,16)-graphs, represented here by

   ```text
   OsHHirKdlp[IFVI|KpqfR
   Ov?IXZIhlRWjUXL[iphst
   ```

5. For each core, the only unknown edges are the 64 cross edges between `A` and the core. The generator enumerates all 872 possible mixed homogeneous 4-sets and adds one clause for each vertex-disjoint pair. Each CNF has 104,524 clauses.

UNSAT for both CNFs rules out every possible counterexample. Since `z(19)=6` and `z(n)` is nondecreasing, this gives `z(20)=6`.

## Files

- `generate.py`: dependency-free graph6 decoder and deterministic CNF generator.
- `audit.py`: regenerates each CNF exactly and compares its semantics with direct graph enumeration on 1,000 deterministic random assignments per core.
- `z20_core0.cnf`, `z20_core1.cnf`: the two fixed-core SAT instances.
- `z20_core0.drup`, `z20_core1.drup`: tree-like DRUP proofs ending in the empty clause.
- `dpll_drup.c`: complete DPLL solver that produced the proofs.
- `check_drup.c`: separately written forward RUP checker.
- `results.txt`: generation, solver and checker output.
- `MANIFEST.sha256`: hashes of the package files.

## Reproduce

```sh
python3 generate.py
python3 audit.py
cc -O3 -march=native -Wall -Wextra dpll_drup.c -o dpll_drup
cc -O3 -march=native -Wall -Wextra check_drup.c -o check_drup

./dpll_drup z20_core0.cnf regenerated_core0.drup || test $? -eq 20
./dpll_drup z20_core1.cnf regenerated_core1.drup || test $? -eq 20
cmp z20_core0.drup regenerated_core0.drup
cmp z20_core1.drup regenerated_core1.drup

./check_drup z20_core0.cnf z20_core0.drup
./check_drup z20_core1.cnf z20_core1.drup
sha256sum -c MANIFEST.sha256
```

The proof files use only reverse unit propagation (RUP), so any standard DRAT checker should accept them. A publication workflow should additionally run, for example:

```sh
drat-trim z20_core0.cnf z20_core0.drup
drat-trim z20_core1.cnf z20_core1.drup
```

## Trust boundary

The computational UNSAT step is certificate-backed. A complete published proof still needs an independent audit of the reduction and generator, standard third-party proof checking, and an explicit citation or independently certified reproduction of the completeness of the two Ramsey(4,4,16) cores.
