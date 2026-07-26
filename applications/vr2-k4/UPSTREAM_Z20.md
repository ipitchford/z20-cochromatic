<!-- SPDX-License-Identifier: CC0-1.0 -->

# Upstream z20 dependency

The upper bound in this companion candidate reuses the two-core reduction,
catalogue record, CNFs, and proof objects from the public z20 candidate
release. It is not a new independent reproduction of that upper-bound
computation.

- Repository: `ipitchford/z20-cochromatic`
- Annotated tag: `candidate-2026-07-26`
- Commit: `3c7e520fdc0615f5c700761c2b1e5108dcc836e7`
- Release: <https://github.com/ipitchford/z20-cochromatic/releases/tag/candidate-2026-07-26>
- Upstream status: unrefereed candidate; no external reproduction,
  complete human mathematical verification, or end-to-end formalisation
  is claimed

The full commit hash is the authoritative pin. The annotated tag is not
cryptographically signed.

## Exact artifacts

All paths below are repository-root paths at the pinned commit.

| Artifact | SHA-256 |
|---|---|
| `RELEASE_MANIFEST.sha256` | `69724d37493029cca840e2774a75229d7296be4089e800bcb82ceb54fe709040` |
| `AI_INDEX.md` | `b3a0134d9cfda293333edea5ba18eff41b46a4d5aa59f2bd1b691a9c93db4ca2` |
| `paper/z20_equals_6_proof.pdf` | `045e826bd5d249456ae4759155256d7562c95b850fc83fa1de39283dd7691db3` |
| `paper/z20_equals_6_proof.tex` | `fdbe212ffca1fb7d6b4724054f6fdb1b3ae4eff8ab03939e92208e81398ffdb6` |
| `paper/z20_equals_6_replay_receipt_2026-07-26.md` | `2ad26844ecdceb934d70b227753e256a65b201e7e6a09c448eb5fe54f18a00ee` |
| `src/gen44.c` | `5aa096309de6a4185b9bfbe93da78ed2985e16041dd19da4325a4d8d087ce087` |
| `src/gen44_result.txt` | `a626fb0d17f2b589ff9a6b46d22cf30446b373b86ef1773f7be1914d8acbac98` |
| `certificates/generate.py` | `64466b591c6b88818353206781e2156068220c9a6342bc30fee450bc3e6365ee` |
| `certificates/audit.py` | `36611e5d2b0f4443bf3f9d6991a8e3bf062ec7fa2178a051b6879911ac36ce59` |
| `certificates/check_drup.c` | `1a4c1f405bd34dd66fafcdee0e5e75b7998188a665b69ca6bcd7a9f11ecdca57` |
| `verification/verify_certificate.py` | `821a5bb500f011befcf700c84823d4ec7fe9e3757491e8d8fcd768d4c683e913` |
| `certificates/z20_core0.cnf` | `cbfea7b0b2cb712ad8b4f8b129f74c7f010e879064414eaef76e74aa88be3f44` |
| `certificates/z20_core0.drup` | `3f7aa99011da35a3e2746348bab550eab3f918d10e8a6c619041c72e7033649a` |
| `certificates/core0.lrat` | `df04c4615dd6e44fd81c870e0b82433b6116f0bea135550a393a6d41ad7a1d57` |
| `certificates/z20_core1.cnf` | `d3d96a3c2a719c753242673b81aabc3977c5e435bb5996b4c58c85a82d11dc5a` |
| `certificates/z20_core1.drup` | `ebe9821bb9939f1331f9908415cb8499f6c1d216c0143a0d048ff47533df446b` |
| `certificates/core1.lrat` | `72b7cc4fcce0c4558b457bc14f6c795bc7401b1e7d990c5b679ebbda3708e06c` |

The six CNF/DRUP/LRAT objects, `src/gen44.c`, and
`src/gen44_result.txt` are byte-identical between the historical public
snapshot `8d9829edebecdfc78384eef5b41617ddd32b11ea` recorded by the replay
receipt and the pinned archival commit above. The later commit adds the
complete public release packaging and a portable, fail-closed verifier.

## Verification routes

From a fresh clone of the pinned tag:

```bash
git clone --branch candidate-2026-07-26 --depth 1 \
  https://github.com/ipitchford/z20-cochromatic.git
cd z20-cochromatic
shasum -a 256 -c RELEASE_MANIFEST.sha256
(cd certificates && shasum -a 256 -c MANIFEST.sha256)
python3 verification/verify_certificate.py
```

On GNU/Linux, use `sha256sum -c` instead of `shasum -a 256 -c`.

The third-party tools nauty, `geng`, DRAT-trim, and `cake_lpr` are not
vendored. The z20 residual cocolourability programs are not dependencies
of this companion result.
