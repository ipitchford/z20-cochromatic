---
schema: z20-ai-index/v1
claim_id: erdos-758-z20
claim: "z(20) = 6"
object: maximum cochromatic number over graphs on 20 vertices
status: unrefereed-candidate-computer-assisted-proof
human_review: no complete human mathematical verification reported
external_reproduction: none reported as of 2026-07-26
end_to_end_formalisation: none
local_replay: completed on macOS arm64 on 2026-07-26
release: candidate-2026-07-26
zenodo_record: https://zenodo.org/records/21647645
zenodo_version_doi: 10.5281/zenodo.21647645
zenodo_concept_doi: 10.5281/zenodo.21647644
zenodo_archive: z20-candidate-2026-07-26.zip
zenodo_archive_sha256: 2b92e5febf5deaeb86db96ef37ddd7df33ac4022453090291c72633fda0310e5
zenodo_published_at: 2026-07-28T14:05:33.246549+00:00
license: CC0-1.0 for original material
---

# AI index: candidate proof that \(z(20)=6\)

> **Read this before starting a new search.** The preserved argument already
> reduces the universal 20-vertex problem to two 64-variable UNSAT instances.
> Validate the existing proof objects before spending compute on global SAT,
> exhaustive graph search, or a new candidate hunt.

Publication under CC0 does **not** upgrade the mathematical status. Treat the
result as a candidate until it has received independent scrutiny.

## Archival identity

| Field | Value |
|---|---|
| Exact version DOI | [`10.5281/zenodo.21647645`](https://doi.org/10.5281/zenodo.21647645) |
| Concept DOI (all versions) | [`10.5281/zenodo.21647644`](https://doi.org/10.5281/zenodo.21647644) |
| Zenodo record | <https://zenodo.org/records/21647645> |
| Deposited archive | `z20-candidate-2026-07-26.zip` |
| Archive SHA-256 | `2b92e5febf5deaeb86db96ef37ddd7df33ac4022453090291c72633fda0310e5` |
| Published | `2026-07-28T14:05:33.246549+00:00` |

The exact version DOI and SHA-256 identify the deposited candidate bytes.
The later GitHub metadata commit that adds these identifiers is not part of
that immutable archive and does not change the archived mathematical claim
or its assurance status.

Related companion result:
[`VR_2(K_4)=20`, exact version DOI `10.5281/zenodo.21647654`](https://doi.org/10.5281/zenodo.21647654).
It is a distinct deposited work with its own concept DOI and
[`AI_INDEX.md`](applications/vr2-k4/AI_INDEX.md).

## Definition and claimed theorem

For a graph \(G\), its cochromatic number \(z(G)\) is the least number of
classes in a partition of \(V(G)\) such that every class induces either a
clique or an independent set. Define

\[
z(n)=\max\{z(G): |V(G)|=n\}.
\]

The candidate theorem is

\[
\boxed{z(20)=6}.
\]

## Proof skeleton

1. **Lower bound.** Paley\((17)\) has no clique or independent set of order
   \(4\), by the hand argument in the paper. Thus every homogeneous class has
   at most three vertices and \(z(\mathrm{Paley}(17))\geq6\). Adding three
   isolated vertices preserves the induced Paley graph, so \(z(20)\geq6\).
   An explicit six-class partition is supplied.

2. **First homogeneous set.** \(R(4,4)=18\), so every 20-vertex graph contains
   a homogeneous 4-set \(A\). Complementation preserves homogeneous sets, so
   \(A\) may be taken to be a clique.

3. **Two fixed cores.** If the other 16 vertices contain a homogeneous 4-set,
   it is disjoint from \(A\). Otherwise they induce a \((4,4)\)-Ramsey graph.
   The replayed catalogue contains exactly two such graphs up to isomorphism.

4. **Two SAT instances.** Once a core is fixed, only the \(4\times16=64\)
   cross edges remain variable. There are 872 possible mixed homogeneous-4
   conditions. A clause is added for every vertex-disjoint pair, producing
   104,524 clauses. A satisfying assignment would be precisely a fixed-core
   counterexample with no two disjoint homogeneous 4-sets. Both formulas are
   UNSAT.

5. **Residual 12 vertices.** Exhaustive computation gives \(z(8)\leq3\).
   Every 12-vertex graph either has a homogeneous 4-set, leaving eight
   vertices, or is one of the 1,449,166 \((4,4)\)-graphs of order 12, all
   checked 4-cocolourable. Hence \(z(12)\leq4\).

6. **Upper bound.** Use two disjoint homogeneous 4-sets as two classes and
   cocolour the remaining 12 vertices with at most four more classes.
   Therefore \(z(20)\leq6\).

## Canonical reading order

| Path | Role |
|---|---|
| `paper/z20_equals_6_proof.pdf` | Canonical human-readable proof and assurance report |
| `paper/z20_equals_6_proof.tex` | Canonical editable source |
| `paper/z20_equals_6_replay_receipt_2026-07-26.md` | Dated one-machine replay receipt |
| `CITATION.cff` | Exact version DOI, concept DOI, and preferred citation |
| `README.md` | Repository overview and build commands |
| `z20_proof_paper.md` | Earlier manuscript; defer to the canonical paper where wording differs |
| `z20_walkthrough.md` | Expository explanation of the reduction and encoding |
| `certificates/generate.py` | Deterministic construction of the two fixed-core CNFs |
| `certificates/audit.py` | Package regeneration and deterministic semantic audit |
| `certificates/check_drup.c` | Package RUP checker |
| `certificates/z20_core{0,1}.cnf` | Exact formulas whose unsatisfiability is certified |
| `certificates/z20_core{0,1}.drup` | Tree-like RUP/DRUP refutations |
| `certificates/core{0,1}.lrat` | LRAT translations accepted by `cake_lpr` |
| `src/gen44.c`, `src/gen44d.c` | Orderly \((4,4)\)-graph generation using nauty |
| `src/cochk.c` | Exact recursive \(k\)-cocolourability decision procedure |
| `src/*_result.txt` | Preserved catalogue, residual, and lower-bound outputs |
| `verification/verify_certificate.py` | Separately implemented formula construction, semantic comparison, and RUP checking |
| `lean_blueprint.md` | Formalisation plan only; it is not a Lean proof |

`z20_investigation.md` records search history and failed approaches. It is not
load-bearing for the final argument.

## Path map from the paper's local bundle

The paper records the layout of `/Users/admin/z20_repro`. This public
repository uses shorter paths:

| Local-bundle path in the paper | Public repository path |
|---|---|
| `nauty/gen44.c` | `src/gen44.c` |
| `nauty/gen44d.c` | `src/gen44d.c` |
| `nauty/cochk.c` | `src/cochk.c` |
| `nauty/*_result.txt` | `src/*_result.txt` |
| `certificate/z20_core_certificate_candidate/*` | `certificates/*` |
| `drat/mine_core0.cnf`, `drat/mine_core1.cnf` | byte-identical to `certificates/z20_core0.cnf`, `certificates/z20_core1.cnf` |
| `cake_lpr/core0.lrat`, `cake_lpr/core1.lrat` | `certificates/core0.lrat`, `certificates/core1.lrat` |

DRAT-trim, `cake_lpr`, nauty, and `geng` are referenced third-party tools;
their sources and binaries are not vendored.

## Exact fixed-core data

Core 0:

```text
graph6: OsHHirKdlp[IFVI|KpqfR
CNF SHA-256:  cbfea7b0b2cb712ad8b4f8b129f74c7f010e879064414eaef76e74aa88be3f44
DRUP SHA-256: 3f7aa99011da35a3e2746348bab550eab3f918d10e8a6c619041c72e7033649a
LRAT SHA-256: df04c4615dd6e44fd81c870e0b82433b6116f0bea135550a393a6d41ad7a1d57
```

Core 1:

```text
graph6: Ov?IXZIhlRWjUXL[iphst
CNF SHA-256:  d3d96a3c2a719c753242673b81aabc3977c5e435bb5996b4c58c85a82d11dc5a
DRUP SHA-256: ebe9821bb9939f1331f9908415cb8499f6c1d216c0143a0d048ff47533df446b
LRAT SHA-256: 72b7cc4fcce0c4558b457bc14f6c795bc7401b1e7d990c5b679ebbda3708e06c
```

Each core has 16 vertices, 60 edges, degree sequence \(7^8 8^8\), 56
triangles, 56 independent triples, and no homogeneous 4-set.

For each core:

```text
cross-edge variables: 64
mixed homogeneous-4 conditions: 872
condition split: 64 + 360 + 224 + 224
clauses: 104,524
clause lengths: 43,840 of length 6; 52,416 of length 7; 8,268 of length 8
```

## Exact catalogue and residual counts

These are counts of **unlabelled graphs up to isomorphism**:

```text
n:      1  2  3  4  5  6   7    8     9      10      11       12
count:  1  2  4  9 24 84 362 2079 14701  103706  546356  1449166

n:       13      14   15  16 17 18
count: 1184231 130816 640   2  1  0
```

The order-17 survivor and empty order-18 level jointly re-establish
\(R(4,4)=18\).

Residual checks recorded in the replay receipt:

```text
all simple graphs on 8 vertices: 12,346 checked; 0 not 3-cocolourable
(4,4)-graphs on 12 vertices: 1,449,166 checked; 0 not 4-cocolourable
Paley-derived graphs of orders 17–20: 4/4 not 5-cocolourable; 4/4 6-cocolourable
```

The lower bound in the canonical paper is hand-checkable; the last
computation is only a cross-check.

## Certificate verdicts

The 26 July 2026 replay recorded:

| Check | Core 0 | Core 1 |
|---|---|---|
| Package RUP checker | `VERIFIED`, 1,571 proof lines | `VERIFIED`, 789 proof lines |
| Separate formula/RUP implementation | identical 104,524-clause set; empty clause in 1,571 steps | identical 104,524-clause set; empty clause in 789 steps |
| Direct semantic comparison | 300/300 assignments agreed | 300/300 assignments agreed |
| `drat-trim` | `s VERIFIED`; 1,467/1,572 lemmas in core; 11,694 resolution steps; 0 RAT | `s VERIFIED`; 752/790 lemmas in core; 5,705 resolution steps; 0 RAT |
| `cake_lpr` on corresponding LRAT | exact text `s VERIFIED UNSAT` | exact text `s VERIFIED UNSAT` |

The package audit also regenerated both formulas byte-for-byte, tested 1,000
deterministic semantic assignments per core, and passed its twelve-entry
manifest. LRAT regeneration was byte-for-byte identical.

A cross-core formula/proof pairing was rejected by the RUP checker and
`drat-trim`; `cake_lpr` printed a checking failure. **Do not use `cake_lpr`
process status alone:** it may return status 0 on failure. Require the exact
success line `s VERIFIED UNSAT`.

## Hashes of the canonical report artifacts

```text
045e826bd5d249456ae4759155256d7562c95b850fc83fa1de39283dd7691db3  paper/z20_equals_6_proof.pdf
fdbe212ffca1fb7d6b4724054f6fdb1b3ae4eff8ab03939e92208e81398ffdb6  paper/z20_equals_6_proof.tex
2ad26844ecdceb934d70b227753e256a65b201e7e6a09c448eb5fe54f18a00ee  paper/z20_equals_6_replay_receipt_2026-07-26.md
```

The replay report was prepared from local commit `61e8300` and reviewed the
earlier public snapshot `8d9829edebecdfc78384eef5b41617ddd32b11ea`.

## Trust boundary

Established by direct mathematics in the canonical report:

- definitions and complement/induced-subgraph invariances;
- the Paley(17) lower bound;
- the structural reduction to two 16-vertex cores;
- the classification of the 872 mixed conditions;
- the equivalence between satisfying assignments and fixed-core
  counterexamples; and
- the final deduction from two disjoint homogeneous 4-sets and
  \(z(12)\leq4\).

Established for the **exact supplied CNFs**:

- each DRUP refutation is accepted by two separately implemented RUP
  checkers and by DRAT-trim; and
- the corresponding LRAT proof is accepted against the exact CNF by the
  formally verified `cake_lpr` core.

Not formally verified end to end:

- correctness of `gen44.c`, `gen44d.c`, nauty canonicalisation, or
  `cochk.c`;
- correctness of the source implementation of the graph-to-CNF
  translation;
- compiler, operating system, file I/O, and hardware; and
- the full theorem inside Lean or another proof assistant.

Semantic tests and agreement with known catalogue data are strong
validation, but they are not formal proofs of those implementations. A valid
LRAT proof establishes the CNF's unsatisfiability; the written reduction and
encoding equivalence connect that CNF fact to \(z(20)\).

## Minimal reproduction order

Use the lowest sufficient tier for your purpose.

1. **Understand, no compute.** Read this file, the replay receipt, and the
   canonical PDF or TeX. Do not restart the original global search.

2. **Integrity only.**

   On macOS:

   ```bash
   (cd certificates && shasum -a 256 -c MANIFEST.sha256)
   shasum -a 256 -c RELEASE_MANIFEST.sha256
   ```

   On GNU/Linux:

   ```bash
   (cd certificates && sha256sum -c MANIFEST.sha256)
   sha256sum -c RELEASE_MANIFEST.sha256
   ```

3. **Portable semantic and RUP replay.** Install NumPy, then run:

   ```bash
   python3 verification/verify_certificate.py
   ```

   The default certificate directory is repository-relative. An alternate
   package directory may be supplied as the first argument. The checker exits
   nonzero if any regenerated-clause, manifest, semantic, or RUP check fails.

4. **Package audit and checker.**

   ```bash
   (cd certificates && python3 audit.py)
   cc -O3 -Wall -Wextra certificates/check_drup.c -o /tmp/z20_check_drup
   /tmp/z20_check_drup certificates/z20_core0.cnf certificates/z20_core0.drup
   /tmp/z20_check_drup certificates/z20_core1.cnf certificates/z20_core1.drup
   ```

5. **Third-party certificate verification.** Obtain DRAT-trim and `cake_lpr`
   from their upstream projects; they are not vendored. Check both matched
   pairs:

   ```bash
   drat-trim certificates/z20_core0.cnf certificates/z20_core0.drup
   drat-trim certificates/z20_core1.cnf certificates/z20_core1.drup
   cake_lpr certificates/z20_core0.cnf certificates/core0.lrat
   cake_lpr certificates/z20_core1.cnf certificates/core1.lrat
   ```

   Require `s VERIFIED` from DRAT-trim and the exact text
   `s VERIFIED UNSAT` from `cake_lpr`. Cross-pair one formula and the other
   proof as a negative control; it must be rejected.

6. **Full combinatorial reproduction.** Only if independent end-to-end
   reproduction is the goal, build nauty, `src/gen44.c`, `src/gen44d.c`, and
   `src/cochk.c`; replay the order-16 through order-18 catalogue, the
   12,346-graph \(z(8)\) check, and the 1,449,166-graph residual \(z(12)\)
   check. Expected outputs are above and in `src/*_result.txt`.

`certificates/generate.py` writes CNFs beside itself. Run it in a scratch
copy if you want to preserve the checked-in files unchanged.

## CC0 reuse

See [`LICENSE`](LICENSE) and [`PUBLIC_DOMAIN.md`](PUBLIC_DOMAIN.md). To the
extent legally possible, all original repository content is dedicated to
the public domain under **CC0-1.0**. It may be copied, redistributed,
translated, incorporated into datasets, ported to proof assistants, or
modified without asking permission.

Third-party tools and embedded font software retain their own licences. CC0
supplies no warranty and does not make the candidate proof reviewed or
correct. Attribution is not required, but preserving this index, artifact
hashes, provenance, and the candidate-status label helps later humans and
AIs distinguish exact reuse from independent verification.
