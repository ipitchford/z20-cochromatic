---
schema: vr2-k4-ai-index/v1
claim: "VR_2(K_4) = 20"
status: unrefereed-candidate-computer-assisted-result
human_review: no complete human mathematical verification reported
external_reproduction: none reported as of 2026-07-26
end_to_end_formalisation: none
lower_bound: new hand-checkable 19-vertex construction with direct verifier
upper_bound: reused fixed-core z20 dependency
upstream_tag: candidate-2026-07-26
upstream_commit: 3c7e520fdc0615f5c700761c2b1e5108dcc836e7
zenodo_record: https://zenodo.org/records/21647654
zenodo_version_doi: 10.5281/zenodo.21647654
zenodo_concept_doi: 10.5281/zenodo.21647653
zenodo_archive: z20-vr2-k4-v0.1-candidate.zip
zenodo_archive_sha256: e14178610233f9e5960da06162e07f3a0ce9aa65799dff3d456958a417997f4f
zenodo_published_at: 2026-07-28T14:05:44.865214+00:00
license: CC0-1.0 for original material
---

# AI index: candidate determination of $\mathrm{VR}_2(K_4)=20$

> **Read the dependency split before spending compute.** The new work in
> this directory is the 19-vertex lower construction and its direct
> verifier. The 20-vertex upper bound reuses the exact two-core lemma,
> formulas, and proof objects already published in the parent z20 candidate
> release.

Publication under CC0 does not upgrade the mathematical status. This is an
unrefereed candidate result offered for scrutiny.

## Archival identity

| Field | Value |
|---|---|
| Exact version DOI | [`10.5281/zenodo.21647654`](https://doi.org/10.5281/zenodo.21647654) |
| Concept DOI (all versions) | [`10.5281/zenodo.21647653`](https://doi.org/10.5281/zenodo.21647653) |
| Zenodo record | <https://zenodo.org/records/21647654> |
| Deposited archive | `z20-vr2-k4-v0.1-candidate.zip` |
| Archive SHA-256 | `e14178610233f9e5960da06162e07f3a0ce9aa65799dff3d456958a417997f4f` |
| Published | `2026-07-28T14:05:44.865214+00:00` |

This metadata identifies the immutable deposited candidate package. The
later GitHub metadata commit is not inside the Zenodo archive and is not a
new verification event.

## Definition and claim

For a graph $F$ without isolated vertices, $\mathrm{VR}_t(F)$ is the
least $n$ such that every red-blue edge-colouring of $K_n$ contains
$t$ pairwise vertex-disjoint monochromatic copies of $F$. The copies
need not receive the same colour.

The candidate claim is:

$$
\boxed{\mathrm{VR}_2(K_4)=20}.
$$

## Proof skeleton

1. **Lower bound.** Replace one vertex of the Paley graph $P_{17}$ by
   three independent twins. Every monochromatic $K_4$ in the resulting
   19-vertex colouring contains at least two twins, so no two are
   vertex-disjoint.
2. **First homogeneous set.** $R(4,4)=18$, so every 20-vertex colouring
   has a monochromatic $K_4$.
3. **Two fixed cores.** If the remaining 16 vertices contain another
   homogeneous four-set, the target pair already exists. Otherwise they
   induce one of exactly two $(4,4)$-Ramsey graphs.
4. **Two SAT instances.** Each core leaves 64 cross-edge variables and
   yields a 104,524-clause CNF. The pinned DRUP/LRAT proof objects certify
   both exact CNFs as unsatisfiable.

## New lower-bound artifact

Canonical verifier:
[`verify_lower_bound.py`](verify_lower_bound.py)

Expected exact output:
[`verifier_output.txt`](verifier_output.txt)

The verifier is standard-library-only. It enumerates all 3,876 four-sets
and reports:

```text
vertices: 19
red edges: 84
degree sequence: (8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 10, 10, 10, 10, 10, 10, 10, 10)
red K4s: 0
blue K4s: 44
disjoint monochromatic pair exists: False
graph6: RzlXWmJpZDeJEJbDgp\EJsWnDlEJY?
All checks passed.
```

Its explicit runtime checks remain active under `python3 -O`, and any
failed invariant produces a nonzero process status.

## Reused upper-bound dependency

The authoritative dependency map is
[`UPSTREAM_Z20.md`](UPSTREAM_Z20.md).

- repository: `ipitchford/z20-cochromatic`
- annotated tag: `candidate-2026-07-26`
- full commit: `3c7e520fdc0615f5c700761c2b1e5108dcc836e7`
- upstream status: unrefereed candidate

The companion does not independently reproduce the parent catalogue or
certificate computation and does not upgrade its status. The parent’s
load-bearing generator, exact CNFs, DRUP/LRAT proof objects, package audit,
and separate verifier are referenced by immutable commit plus SHA-256.

## Canonical reading order

| Path | Role |
|---|---|
| `README.md` | Status, proof split, authorship, commands, and CC0 scope |
| `paper.pdf` | Human-readable candidate paper |
| `paper.tex` | Editable source |
| `CITATION.cff` | Exact version DOI, concept DOI, and preferred citation |
| `verify_lower_bound.py` | Direct lower-witness verifier |
| `verifier_output.txt` | Recorded expected output |
| `UPSTREAM_Z20.md` | Exact inherited dependency |
| `MANIFEST.sha256` | Local application integrity boundary |
| `../../AI_INDEX.md` | Parent z20 claim/evidence map |

## Minimal verification order

1. Read `README.md`, this file, and the paper’s assurance section.
2. Check local integrity:

   ```bash
   cd applications/vr2-k4
   shasum -a 256 -c MANIFEST.sha256
   ```

3. Replay only the new lower witness:

   ```bash
   python3 verify_lower_bound.py
   ```

4. Before replaying the upper-bound dependency, verify the pinned tag,
   commit, and hashes in `UPSTREAM_Z20.md`.
5. Use the parent `verification/verify_certificate.py` for the shortest
   semantic/RUP replay. Full catalogue regeneration is necessary only for
   a genuinely independent end-to-end reproduction.

## Trust boundary

Directly inspectable in this companion:

- the definition and reduction;
- the Paley-twin lower construction;
- enumeration of every four-set in the lower verifier; and
- the mapping from the upper-bound lemma to the pinned parent artifacts.

Inherited from the parent candidate:

- catalogue generation and nauty canonicalisation;
- graph-to-CNF implementation;
- the exact CNFs and refutations;
- compiler, operating-system, file-I/O, and hardware assumptions; and
- the absence of end-to-end proof-assistant formalisation.

A valid LRAT proof establishes unsatisfiability of an exact CNF. The
written graph-theoretic reduction and encoding equivalence remain the
bridge from that CNF fact to the claimed theorem.

## CC0 reuse

All original companion material is dedicated under CC0-1.0 to the extent
legally possible. Embedded font software, cited works, linked external
material, and third-party tools retain their own terms. Preserve the
candidate-status and dependency metadata when distinguishing reuse from
new verification.
