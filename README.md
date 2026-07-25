# z(20) = 6 — a candidate computer-assisted proof

The **cochromatic number** `z(G)` of a graph is the least number of classes in a partition
of its vertices where every class induces a clique or an independent set. Let
`z(n) = max{ z(G) : |V(G)| = n }`.

The values `z(1..19)` are known. Whether `z(20) = 6` or `7` was open — it is the open
sub-question recorded on [Erdős Problem #758](https://www.erdosproblems.com/758).

**This repository contains a candidate proof that `z(20) = 6`, together with everything
needed to check it.**

> **Status: unrefereed, and not yet verified by a human mathematician.**
> Every mathematical step was produced by AI systems (see [Provenance](#provenance)).
> It is published here for scrutiny. A demonstration that it is *wrong* would be at least
> as useful as confirmation.

## The argument in brief

**Upper bound.** Let `G` have 20 vertices.

1. `20 ≥ R(4,4) = 18`, so `G` has a homogeneous 4-set `A`. The property "has two disjoint
   homogeneous 4-sets" is complement-invariant, so WLOG `A` is a clique; relabel
   `A = {0,1,2,3}`.
2. If the other 16 vertices contain a homogeneous 4-set, it is disjoint from `A` and we are
   done. Otherwise they induce a **(4,4)-Ramsey graph on 16 vertices** — and there are
   exactly **two** of those up to isomorphism.
3. Fixing each core leaves only the `4 × 16 = 64` cross edges. Enumerating the mixed sets
   that can be homogeneous gives **872 conditions** per core; forbidding every
   vertex-disjoint pair yields a CNF of **104,524 clauses over 64 variables**. Both
   instances are **UNSAT**.
4. Hence every 20-vertex graph has *two disjoint* homogeneous 4-sets. Take them as two
   classes; the remaining 12 vertices need at most `z(12) = 4`. So **`z(20) ≤ 6`**.

**Lower bound — entirely hand-verifiable, no computation required.**
Paley(17) is edge-transitive under `x ↦ ax+b` (`a` a quadratic residue), so a hypothetical
`K₄` may be assumed to contain the edge `{0,1}`. The common neighbours of 0 and 1 are
`Q ∩ (1+Q) = {2, 9, 16}`, whose pairwise differences are 7 and 14 — neither a quadratic
residue. So those three are pairwise non-adjacent and no `K₄` exists. Multiplication by a
non-residue is an isomorphism to the complement, so there is no independent 4-set either.
Hence every homogeneous set has ≤ 3 vertices and `z(Paley(17)) ≥ ⌈17/3⌉ = 6`; monotonicity
under induced subgraphs lifts this to `Paley(17) + 3K₁` on 20 vertices.

Matching **six-class certificate** (vertices 17,18,19 isolated), so the value is exactly 6:

```
I₁ = {0,3,6,17,18,19}   I₂ = {1,4,7}     I₃ = {2,9,12}
I₄ = {5,8,11}           I₅ = {10,13,16}  K₁ = {14,15}
```

The first five are independent, the last is an edge. This makes the entire lower bound
checkable by hand, with no reliance on `cochk` or any solver.

## What was recomputed rather than cited

No *mathematical* input is taken on trust — every combinatorial fact below was
regenerated locally from its definition rather than cited:

| input | how established here |
|---|---|
| `R(4,4) = 18` | orderly generation — level 18 is empty |
| exactly two (4,4)-graphs on 16 vertices | orderly generation from scratch |
| the two refutations | three independent checkers (see below) |
| `z(8) ≤ 3` | all 12,346 graphs on 8 vertices |
| `z(12) ≤ 4` | case split + all 1,449,166 (4,4)-graphs on 12 vertices |
| `z(20) ≥ 6` | hand proof + explicit 6-class certificate (above); no solver needed |

The generator reproduces the published (4,4,n) sequence in full:

```
n :  1  2  3  4  5  6   7    8     9     10      11       12       13     14   15 16 17 18
# :  1  2  4  9 24 84 362 2079 14701 103706  546356  1449166  1184231 130816 640  2  1  0
```

The **2** at n=16 matches McKay's `r44_16.g6` character for character; n=17 is Paley(17);
the **0** at n=18 re-derives `R(4,4) = 18`.

**What this does and does not claim.** Regenerating every combinatorial input, matching the
published Ramsey sequence, and passing independent proof checkers is strong *validation* of
the software; it is not a *proof* that the software is correct. A correlated implementation
error in the generator, the graph-to-CNF translation, or the cocolourability checker remains
logically possible. The accurate description is:

> a complete, locally regenerated computer-assisted proof of `z(20) = 6`, with
> independently checked SAT refutations

rather than a claim that the operating system, compiler, libraries and custom encoders have
themselves been verified. `drat-trim` and `cake_lpr` certify the **SAT layer**; the
**encoding lemmas** — that the CNFs mean what they are said to mean — are validated by
semantic spot-testing, not proved.

## Verification of the two refutations

Each was checked against CNFs **regenerated independently** from the graph6 strings, not
against the original files:

| checker | core 0 | core 1 |
|---|---|---|
| hand-written RUP checker | verified | verified |
| `drat-trim` | `s VERIFIED` | `s VERIFIED` |
| `cake_lpr` (formally verified core) | `s VERIFIED UNSAT` | `s VERIFIED UNSAT` |

Negative controls — cross-core proof/CNF pairings, truncated proofs, injected clauses —
were correctly rejected by every checker. `drat-trim` reports **0 RAT lemmas**, so the
certificates lie in the RUP fragment.

## Contents

| path | what it is |
|---|---|
| `z20_proof_paper.md` | the formal write-up |
| `z20_walkthrough.md` / `.pdf` | expository walkthrough, including the SAT encoding built by hand |
| `z20_investigation.md` | narrative account, including the search approach that failed |
| `lean_blueprint.md` | plan for a Lean 4 / Mathlib formalisation |
| `src/gen44.c`, `gen44d.c` | orderly generation of (4,4)-graphs (needs nauty ≥ 2.9) |
| `src/cochk.c` | exact k-cocolourability decision from graph6 on stdin |
| `src/*_result.txt` | result logs for each computation |
| `certificates/z20_core{0,1}.cnf` | the two SAT instances |
| `certificates/z20_core{0,1}.drup` | the DRUP refutations |
| `certificates/core{0,1}.lrat` | LRAT translations (via `drat-trim -L`) |
| `certificates/generate.py` | the original CNF generator |
| `verification/verify_certificate.py` | independent CNF regeneration + semantic test + RUP checker |
| `verification/c6_fast.py` | exact counter for 6-cocolourings (memoised subset DP) |

Third-party tools are not vendored — get them from source:
[nauty](https://pallini.di.uniroma1.it/),
[drat-trim](https://github.com/marijnheule/drat-trim),
[cake_lpr](https://github.com/tanyongkiam/cake_lpr).

## Reproducing

```bash
# the (4,4,n) sequence, the two 16-vertex cores, and R(4,4)=18
cc -O3 -I/path/to/nauty -o gen44 src/gen44.c -L/path/to/nauty -lnauty
./gen44 18

# z(8) <= 3   (all 12,346 graphs on 8 vertices)
cc -O3 -o cochk src/cochk.c
geng -q 8 | ./cochk 3

# z(12) <= 4  (all 1,449,166 (4,4)-graphs on 12 vertices)
cc -O3 -I/path/to/nauty -o gen44d src/gen44d.c -L/path/to/nauty -lnauty
./gen44d 12 12 | ./cochk 4

# the refutations
drat-trim certificates/z20_core0.cnf certificates/z20_core0.drup
cake_lpr  certificates/z20_core0.cnf certificates/core0.lrat
```

`verification/verify_certificate.py` regenerates both CNFs independently, spot-checks the
encoding semantically against direct computation on 20-vertex graphs, and RUP-checks the
DRUP proofs against its own CNFs.

## Open work

The Lean formalisation ([`lean_blueprint.md`](lean_blueprint.md)) decomposes into a
skeleton plus four computational obligations. The SAT refutations look tractable — see
**LRAT-Catcher** ([arXiv:2607.00815](https://arxiv.org/abs/2607.00815)), which imports a
DIMACS formula plus LRAT certificate into Lean 4 as an actual theorem by reflection, and
was demonstrated on `R(4,4) = 18` — one of the very obligations here. The
**enumeration obligations are the bottleneck**, as they need verified isomorph-free graph
generation. Note that a Lean theorem about a CNF is not yet a Lean theorem about `z(20)`:
the encoding-soundness lemmas would still need formalising. There may also be a route that avoids
the 16-vertex catalogue entirely by proving "every 20-vertex graph has two disjoint
homogeneous 4-sets" as a single UNSAT over 190 variables — attempted here without
termination under weak symmetry breaking, but plausibly within reach of SMS-style dynamic
canonicity.

## Provenance

Every mathematical step was produced by AI systems. The human participant selected the
problem and mediated between systems, and claims none of the mathematics.

- **Phase 1 (unsuccessful).** A Nous Hermes agent designed a CEGIS harness driving OpenAI's
  GPT-5.6 Sol. About two days and ~42 million learned clauses, no result. Its progress
  metric was later shown to be invalid — five of its six best candidates were provably
  6-cocolourable before any checking.
- **Phase 2.** Claude 4.8: instrumentation, baselines, characterisation of the candidates.
- **Phase 3 (the reduction).** GPT-5.6 Sol, contributing directly: the two-core reduction,
  the CNF generator, the DPLL solver, the DRUP certificates.
- **Phase 4 (verification).** Claude Opus 5: independent verification, the catalogue and
  `R(4,4) = 18` recomputation, the `z(8)` and `z(12)` re-derivations, the lower bound, and
  the write-ups.

No step of the final argument rests on an assertion by a language model that was not
subsequently recomputed by a *different* system than the one that asserted it.

## Licence

Public domain (CC0). Third-party tools retain their own licences.
