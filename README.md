# z(20) = 6 — a candidate computer-assisted proof

[![DOI: all z(20)=6 versions](https://zenodo.org/badge/DOI/10.5281/zenodo.21647644.svg)](https://doi.org/10.5281/zenodo.21647644)

The **cochromatic number** `z(G)` of a graph is the least number of classes in a partition
of its vertices where every class induces a clique or an independent set. Let
`z(n) = max{ z(G) : |V(G)| = n }`.

The case `z(20)`, previously known only to be `6` or `7`, is the sub-question
recorded on [Erdős Problem #758](https://www.erdosproblems.com/758).

**This repository contains a candidate proof that `z(20) = 6`, together with
the source, proof objects, and replay records needed to scrutinise it.**

> [!IMPORTANT]
> **Evidence status:** This is an **unrefereed candidate computer-assisted
> proof**. A dated replay has been completed on one macOS/arm64 machine. No
> human mathematician has verified the complete argument; no independent
> external reproduction or end-to-end proof-assistant formalisation is
> claimed. The SAT certificates establish the unsatisfiability of the two
> exact CNFs. The graph-theoretic reduction and encoding equivalence are
> separate obligations discussed in the paper.
>
> **Automated readers and AI systems:** start with
> [`AI_INDEX.md`](AI_INDEX.md) for the claim/evidence map, exact hashes,
> public-path mapping, trusted-computing boundary, and shortest
> non-duplicative verification route.

**Machine-readable claims:** [`CLAIMPACK.md`](CLAIMPACK.md) links to the
ClaimPack mirrors for both candidate results and their pinned validator.

**Primary release artifacts:**
[candidate paper (PDF)](paper/z20_equals_6_proof.pdf) ·
[LaTeX source](paper/z20_equals_6_proof.tex) ·
[dated replay receipt](paper/z20_equals_6_replay_receipt_2026-07-26.md)

**Archived candidate release:** exact version DOI
[`10.5281/zenodo.21647645`](https://doi.org/10.5281/zenodo.21647645);
archive `z20-candidate-2026-07-26.zip`; SHA-256
`2b92e5febf5deaeb86db96ef37ddd7df33ac4022453090291c72633fda0310e5`.
The concept DOI above resolves to the version family. The exact version DOI
and archive hash identify the fixed deposited bytes.

## Companion applications

### Two vertex-disjoint monochromatic K4s

[![DOI: all VR2(K4)=20 versions](https://zenodo.org/badge/DOI/10.5281/zenodo.21647653.svg)](https://doi.org/10.5281/zenodo.21647653)

[`applications/vr2-k4/`](applications/vr2-k4/) contains an unrefereed
companion candidate determination of
$\mathrm{VR}_2(K_4)=20$. It adds a hand-checkable 19-vertex lower
construction, a dependency-free verifier, and its own
[AI index](applications/vr2-k4/AI_INDEX.md).

Its exact archived candidate release is
[`10.5281/zenodo.21647654`](https://doi.org/10.5281/zenodo.21647654);
archive `z20-vr2-k4-v0.1-candidate.zip`; SHA-256
`e14178610233f9e5960da06162e07f3a0ce9aa65799dff3d456958a417997f4f`.

Its 20-vertex upper bound reuses—not independently reproduces—the exact
two-core reduction and certificate artifacts pinned to z20 tag
[`candidate-2026-07-26`](https://github.com/ipitchford/z20-cochromatic/tree/candidate-2026-07-26),
commit `3c7e520fdc0615f5c700761c2b1e5108dcc836e7`.

No external reproduction, complete human mathematical verification, peer
review, or end-to-end formalisation is claimed.

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

The finite combinatorial inputs reported below were regenerated locally from
their definitions rather than simply imported from published tables. This
describes the recorded one-machine replay; it is not independent external
reproduction and does not formally verify the custom programs.

| input | how established here |
|---|---|
| `R(4,4) = 18` | orderly generation — level 18 is empty |
| exactly two (4,4)-graphs on 16 vertices | orderly generation from scratch |
| the two refutations | two RUP checkers and DRAT-trim on DRUP; `cake_lpr` on corresponding LRAT |
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

> a complete, locally regenerated candidate computer-assisted proof of
> `z(20) = 6`, with certificate-backed SAT refutations

rather than a claim that the operating system, compiler, libraries and custom encoders have
themselves been verified. `drat-trim` and `cake_lpr` certify the **SAT layer**; the
**encoding lemmas** — that the CNFs mean what they are said to mean — are validated by
semantic spot-testing, not proved.

## Verification of the two refutations

Each preserved DRUP proof was checked against separately regenerated CNFs.
The corresponding LRAT proof was also checked against the exact CNF:

| checker | core 0 | core 1 |
|---|---|---|
| separately implemented Python RUP checker | verified | verified |
| package C RUP checker | verified | verified |
| `drat-trim` | `s VERIFIED` | `s VERIFIED` |
| `cake_lpr` on LRAT (formally verified core) | `s VERIFIED UNSAT` | `s VERIFIED UNSAT` |

Negative controls — cross-core proof/CNF pairings, truncated proofs, injected clauses —
were correctly rejected. `cake_lpr` can print a checking failure while returning process
status 0, so automation must require the exact success text `s VERIFIED UNSAT`.
`drat-trim` reports **0 RAT lemmas**, so the certificates lie in the RUP fragment.

## Contents

| path | what it is |
|---|---|
| `paper/z20_equals_6_proof.pdf` | 13-page candidate certificate-backed proof, including its assurance boundary |
| `paper/z20_equals_6_proof.tex` | exact LaTeX source for the candidate paper |
| `paper/z20_equals_6_replay_receipt_2026-07-26.md` | dated one-machine replay record; not external reproduction |
| `CITATION.cff` | machine-readable citation metadata for the z20 release, with the VR2 companion listed separately |
| `AI_INDEX.md` | machine-oriented claim/evidence map, hashes, path mapping, caveats, and shortest verification routes |
| `LICENSE` / `PUBLIC_DOMAIN.md` | CC0 1.0 legal text and the exact public-domain scope |
| `RELEASE_MANIFEST.sha256` | focused integrity manifest for repository metadata, the paper, and proof objects |
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
| `certificates/MANIFEST.sha256` | manifest for the complete original 12-file certificate package |
| `verification/verify_certificate.py` | separate CNF construction + semantic test + RUP checker |
| `verification/c6_fast.py` | exact counter for 6-cocolourings (memoised subset DP) |

Third-party tools are not vendored — get them from source:
[nauty](https://pallini.di.uniroma1.it/),
[drat-trim](https://github.com/marijnheule/drat-trim),
[cake_lpr](https://github.com/tanyongkiam/cake_lpr).

## Reproducing

```bash
# integrity on macOS
(cd certificates && shasum -a 256 -c MANIFEST.sha256)
shasum -a 256 -c RELEASE_MANIFEST.sha256

# integrity on GNU/Linux
(cd certificates && sha256sum -c MANIFEST.sha256)
sha256sum -c RELEASE_MANIFEST.sha256

# portable semantic/RUP replay; exits nonzero on any failed check
python3 verification/verify_certificate.py

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

`verification/verify_certificate.py` separately constructs both CNFs, spot-checks the
encoding semantically against direct computation on 20-vertex graphs, and RUP-checks the
DRUP proofs against those clauses. Its default certificate path is repository-relative;
an alternate package directory may be supplied as its first argument.

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
- **Phase 4 (verification).** Claude Opus 5: verification by a different AI system, the catalogue and
  `R(4,4) = 18` recomputation, the `z(8)` and `z(12)` re-derivations, the lower bound, and
  the write-ups.

No step of the final argument rests on an assertion by a language model that was not
subsequently recomputed by a *different* system than the one that asserted it.

## Public-domain dedication

To the extent that copyright or related rights subsist and are held by this
repository's affirmer, all original contents of this repository—including
material already present before this release, prose, source code, generated
data, CNFs, proof certificates, logs, and release metadata—are dedicated to
the public domain under [CC0 1.0 Universal](LICENSE).

`SPDX-License-Identifier: CC0-1.0`

This dedication covers only rights that may legally be waived. It does not
relicense third-party material. Referenced but unvendored tools—including
nauty, DRAT-trim, and `cake_lpr`—and third-party font software embedded in the
generated PDFs retain their own terms. See
[`PUBLIC_DOMAIN.md`](PUBLIC_DOMAIN.md) for the exact scope. No endorsement is
implied.
