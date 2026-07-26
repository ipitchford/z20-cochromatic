<!-- SPDX-License-Identifier: CC0-1.0 -->

# Two vertex-disjoint monochromatic K4s in K20

This directory presents an unrefereed candidate certificate-backed
determination that

$$
\mathrm{VR}_2(K_4)=20.
$$

Here $\mathrm{VR}_2(K_4)$ is the least $n$ such that every red-blue
edge-colouring of $K_n$ contains two pairwise vertex-disjoint
monochromatic copies of $K_4$; the two copies need not have the same
colour.

> [!IMPORTANT]
> **Status: unrefereed candidate computer-assisted result.**
> The lower-bound construction is hand-checkable and has a dependency-free
> direct verifier. The upper bound reuses the two fixed-core
> unsatisfiability certificates from the candidate `z(20)=6` result. Those
> exact certificates were replayed locally by separately implemented
> checkers, including a formally verified CakeML checking core. The complete
> graph-theoretic result has not been independently reproduced, completely
> verified by a human mathematician, peer reviewed, or formalised end to end
> in a proof assistant.

## Files

| Path | Role |
|---|---|
| [`paper.pdf`](paper.pdf) | Candidate paper and assurance report |
| [`paper.tex`](paper.tex) | Editable LaTeX source |
| [`verify_lower_bound.py`](verify_lower_bound.py) | Standard-library verifier for the new 19-vertex lower witness |
| [`verifier_output.txt`](verifier_output.txt) | Fresh deterministic verifier output |
| [`AI_INDEX.md`](AI_INDEX.md) | Machine-oriented claim, dependency, and trust-boundary map |
| [`UPSTREAM_Z20.md`](UPSTREAM_Z20.md) | Exact parent tag, commit, paths, and SHA-256 dependency hashes |
| [`MANIFEST.sha256`](MANIFEST.sha256) | Hashes of every other file in this directory |

The supplied standalone archive also contained a `basis/` directory.
It is intentionally not duplicated here: the canonical parent paper,
receipt, programs, CNFs, and proof objects already live at repository root
and are pinned exactly in [`UPSTREAM_Z20.md`](UPSTREAM_Z20.md).

## Proof split

### New lower bound

Start with the Paley graph $P_{17}$ and replace vertex 9 by three
independent twins. In the resulting 19-vertex colouring, every
monochromatic $K_4$ is blue and contains at least two of those three
twins, so no two such copies are vertex-disjoint.

The verifier reconstructs this graph from the Paley rule, enumerates all
$\binom{19}{4}=3,876$ four-sets, and checks:

```text
vertices: 19
red edges: 84
red K4s: 0
blue K4s: 44
disjoint monochromatic pair exists: False
graph6: RzlXWmJpZDeJEJbDgp\EJsWnDlEJY?
```

Run it with:

```bash
python3 applications/vr2-k4/verify_lower_bound.py
```

The verifier uses explicit runtime checks and exits nonzero on failure,
including when Python optimisation is enabled.

### Reused upper bound

The $K_{20}$ upper bound is the two-disjoint-homogeneous-$4$-sets lemma
already used by the z20 argument. It is reused rather than independently
reproduced here.

Pinned parent release:

- repository: `ipitchford/z20-cochromatic`
- annotated tag: `candidate-2026-07-26`
- commit: `3c7e520fdc0615f5c700761c2b1e5108dcc836e7`
- [candidate release](https://github.com/ipitchford/z20-cochromatic/releases/tag/candidate-2026-07-26)

| Paper obligation | Pinned repository artifact |
|---|---|
| Two order-16 Ramsey cores and catalogue transcript | [`src/gen44.c`](../../src/gen44.c), [`src/gen44_result.txt`](../../src/gen44_result.txt) |
| Deterministic fixed-core formula generation | [`certificates/generate.py`](../../certificates/generate.py) |
| Core 0 formula and refutations | [`z20_core0.cnf`](../../certificates/z20_core0.cnf), [`z20_core0.drup`](../../certificates/z20_core0.drup), [`core0.lrat`](../../certificates/core0.lrat) |
| Core 1 formula and refutations | [`z20_core1.cnf`](../../certificates/z20_core1.cnf), [`z20_core1.drup`](../../certificates/z20_core1.drup), [`core1.lrat`](../../certificates/core1.lrat) |
| Package regeneration and checking | [`certificates/audit.py`](../../certificates/audit.py), [`certificates/check_drup.c`](../../certificates/check_drup.c) |
| Separate formula construction, semantic checks, and RUP replay | [`verification/verify_certificate.py`](../../verification/verify_certificate.py) |
| Dated one-machine replay record | [`paper/z20_equals_6_replay_receipt_2026-07-26.md`](../../paper/z20_equals_6_replay_receipt_2026-07-26.md) |

The z20 residual cocolourability computations are not dependencies of this
companion result.

## Authorship and provenance

- **Paper author line:** GPT 5.6 Sol and Claude Opus 4.8 / 5
- **Repository maintainer and publisher:** Ian Pitchford
- **Problem selection and research mediation:** Ian Pitchford
- **Mathematical and computational contributions:** the AI systems named
  in the paper’s provenance section
- **External human verification:** none reported

These are repository-reported provenance statements, not an externally
audited authorship determination. Model names are provenance and credit
labels; they do not imply provider endorsement.

## Build and integrity

```bash
cd applications/vr2-k4
shasum -a 256 -c MANIFEST.sha256      # macOS
sha256sum -c MANIFEST.sha256          # GNU/Linux
python3 verify_lower_bound.py

# Optional source rebuild; requires a complete LaTeX installation and
# leaves the preserved, manifest-bound paper.pdf untouched.
build_dir="$(mktemp -d)"
tectonic -X compile --outdir "$build_dir" paper.tex
```

## Licence

`SPDX-License-Identifier: CC0-1.0`

To the extent copyright or related rights subsist and are held by the
repository affirmer, all original contents of this companion directory are
dedicated to the public domain under
[CC0-1.0](../../LICENSE). The exact scope is recorded in
[`PUBLIC_DOMAIN.md`](../../PUBLIC_DOMAIN.md).

The named AI systems are not the legal CC0 affirmer. Font software embedded
in `paper.pdf`, cited works, linked external material, third-party tools,
and model or provider trademarks retain their own terms. The PDF’s original
text and layout are included in the dedication.
