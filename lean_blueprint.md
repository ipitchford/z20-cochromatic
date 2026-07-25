# Formalisation blueprint: z(20) = 6 in Lean 4 / Mathlib

**Purpose.** A working plan for a `sorry`-free Lean formalisation of the result
z(20) = 6 (Erdős Problem #758, open sub-question). This is a design document, not
a formalisation: it fixes the statement, decomposes the proof into lemmas, maps each
lemma onto Mathlib, and — the substantive part — specifies exactly which facts must be
discharged by certified computation and what shape of certificate each needs.

**Health warning on API names.** Mathlib moves. Every identifier below marked ⚠ is from
recollection and must be checked against the current Mathlib before relying on it. The
lemma *structure* is stable; the *names* are not.

---

## 0. Strategy summary

The proof splits into a small human-readable skeleton and four computational obligations.
The skeleton is routine Lean work. The obligations are the project.

| # | obligation | scale | difficulty |
|---|---|---|---|
| **C1** | R(4,4) = 18 | classical | may already be in Mathlib — check first |
| **C2** | exactly two (4,4)-graphs on 16 vertices | ~1.45M graphs at generation peak | **hardest** |
| **C3** | two SAT instances UNSAT | 104,524 clauses × 2 | **easiest** — LRAT already exists |
| **C4** | z(8) ≤ 3 and z(12) ≤ 4 | 12,346 and 1,449,166 graphs | **hard** |

Recommended order: **C3 → C1 → C4(z8) → C4(z12) → C2**, i.e. cheapest-first, so that
early milestones are real and the skeleton can be assembled against stated hypotheses
while the expensive obligations are still open.

---

## 1. Definitions

```lean
import Mathlib

open Finset SimpleGraph

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- A vertex set is homogeneous if it induces a clique or an independent set. -/
def IsHomogeneous (G : SimpleGraph V) (s : Finset V) : Prop :=
  G.IsClique (s : Set V) ∨ G.IsIndepSet (s : Set V)     -- ⚠ IsIndepSet name

/-- A cocolouring with `k` classes: a vertex map whose fibres are all homogeneous. -/
def IsCocolouring (G : SimpleGraph V) {k : ℕ} (f : V → Fin k) : Prop :=
  ∀ i : Fin k, IsHomogeneous G (univ.filter fun v => f v = i)

def Cocolourable (G : SimpleGraph V) (k : ℕ) : Prop :=
  ∃ f : V → Fin k, IsCocolouring G f

/-- Cochromatic number. -/
noncomputable def cochromatic (G : SimpleGraph V) : ℕ :=
  sInf {k | Cocolourable G k}

/-- The extremal quantity: z(n). -/
noncomputable def zmax (n : ℕ) : ℕ :=
  ⨆ G : SimpleGraph (Fin n), cochromatic G
```

`SimpleGraph (Fin n)` is a `Fintype` ⚠, so the `⨆` is a finite sup and well behaved.
Decidability of `IsHomogeneous` on a `Fintype` should be derivable; you will want a
`DecidablePred` instance for `Cocolourable G k` to make any `decide` route viable.

### 1.1 Design note: `Finset`-partition vs. fibre-map

Two encodings of "cocolouring" are available: a `Finset (Finset V)` partition, or the
fibre map above. **Use the fibre map.** It makes "at most k classes" definitionally
`Fin k`, makes refinement trivial (compose with an injection `Fin k ↪ Fin k'`), and
avoids proving partition well-formedness at every step. Convert to the partition view
only if a specific lemma wants it.

---

## 2. Main statement

```lean
theorem zmax_twenty : zmax 20 = 6
```

proved from

```lean
theorem zmax_twenty_le : zmax 20 ≤ 6
theorem zmax_twenty_ge : 6 ≤ zmax 20
```

---

## 3. Lemma DAG

### Skeleton lemmas (no computation)

```lean
/-- L1. Cochromatic number is monotone under induced subgraphs. -/
lemma cochromatic_induced_le (G : SimpleGraph V) (s : Finset V) :
    cochromatic (G.induce (s : Set V)) ≤ cochromatic G
```
*Proof:* restrict a cocolouring; subsets of cliques are cliques, subsets of independent
sets are independent. Needs `SimpleGraph.induce` ⚠ and a lemma that `IsClique` is
downward closed (`IsClique.subset` ⚠).

```lean
/-- L2. Homogeneity is preserved by complementation. -/
lemma isHomogeneous_compl (G : SimpleGraph V) (s : Finset V) :
    IsHomogeneous Gᶜ s ↔ IsHomogeneous G s
```
*Proof:* `IsClique Gᶜ s ↔ IsIndepSet G s` and vice versa. Should be near-`simp`.
This is what licenses the "WLOG the 4-set is a clique" step; make it explicit rather
than folding it into a `wlog` tactic, since the WLOG is over a *property of G*, not a
symmetry of the goal.

```lean
/-- L3. Every graph on ≥18 vertices has a homogeneous 4-set. (From C1.) -/
lemma exists_homogeneous_four (G : SimpleGraph V) (h : 18 ≤ Fintype.card V) :
    ∃ s : Finset V, s.card = 4 ∧ IsHomogeneous G s
```

```lean
/-- L6. Every 20-vertex graph has two DISJOINT homogeneous 4-sets. (From L3, C2, C3.) -/
lemma exists_two_disjoint_homogeneous_four (G : SimpleGraph (Fin 20)) :
    ∃ s t : Finset (Fin 20), s.card = 4 ∧ t.card = 4 ∧ Disjoint s t ∧
      IsHomogeneous G s ∧ IsHomogeneous G t
```

```lean
/-- L9. Upper bound. (From L6, C4.) -/
theorem zmax_twenty_le : zmax 20 ≤ 6
```
*Proof:* given L6, take `s`, `t` as two classes; the induced graph on the remaining 12
vertices is cocolourable in ≤4 by C4; glue. The gluing lemma is worth isolating:

```lean
lemma cochromatic_le_of_split (G : SimpleGraph V) (s : Finset V)
    (hs : IsHomogeneous G s) (k : ℕ)
    (h : Cocolourable (G.induce ((univ \ s : Finset V) : Set V)) k) :
    Cocolourable G (k + 1)
```
Apply twice. This single lemma carries most of the skeleton's real work.

```lean
/-- L11. Lower bound. -/
theorem zmax_twenty_ge : 6 ≤ zmax 20
```
*Proof:* exhibit `paley17 ⊕ (3 isolated vertices)`. Needs
(i) ω(Paley 17) = α(Paley 17) = 3, (ii) a pigeonhole lemma:

```lean
lemma six_le_cochromatic_of_homogeneous_card_le
    (G : SimpleGraph V) (h : ∀ s : Finset V, IsHomogeneous G s → s.card ≤ 3)
    (hn : 17 ≤ Fintype.card V) : 6 ≤ cochromatic G
```
*Proof:* if `f : V → Fin 5` were a cocolouring, the five fibres are homogeneous, so each
has ≤3 elements, so `card V ≤ 15 < 17`. Clean `Finset.card_le_card_of...` argument.
Then L1 lifts it from 17 to 20 vertices.

### The Paley step — hand proof available

ω = α = 3 for Paley(17) need **not** be computational. Paley graphs are
self-complementary (so ω = α), and the clique number of Paley(q) for q = 17 can be
established by a counting/quadratic-residue argument. If formalising the number theory
proves annoying, this is the one computational obligation that is genuinely cheap to
brute-force instead: C(17,4) = 2380 four-sets, trivially `decide`-able.

---

## 4. Computational obligations

### C1. R(4,4) = 18

**Check Mathlib first.** Ramsey number formalisation exists in the Lean ecosystem
(Bhavik Mehta has worked on this — note he is also the author of the z(12) computation
cited on the #758 page). If `R(4,4) = 18` or even just the ≤ direction is available,
L3 is immediate.

Only the **upper** direction is needed: every 2-colouring of K₁₈ has a monochromatic K₄
— equivalently, no (4,4)-graph on 18 vertices exists. If not in Mathlib, note that C2's
generation *also yields this* (level 18 empty), so C1 and C2 can share machinery.

### C2. Exactly two (4,4)-graphs on 16 vertices — **the bottleneck**

Required form:

```lean
lemma r44_16_catalogue (G : SimpleGraph (Fin 16))
    (h : ∀ s : Finset (Fin 16), s.card = 4 → ¬ IsHomogeneous G s) :
    Nonempty (G ≃g core0) ∨ Nonempty (G ≃g core1)
```

Three candidate strategies:

- **(a) Verified orderly generation in Lean.** Mirror the C implementation: extend
  level by level, dedupe by a canonical form, prove that the extension is exhaustive
  (every induced subgraph of a (4,4)-graph is a (4,4)-graph). *Risk:* you must formalise
  a canonical form (a mini-nauty) **and** prove it canonical — that is a substantial
  project in itself, plausibly larger than the rest of the formalisation combined.
  Kernel performance at the 1.45M-graph level is a second, independent risk.

- **(b) Avoid the catalogue entirely.** Prove L6 directly as one UNSAT over the 190 edge
  variables of a 20-vertex graph ("no graph has zero pairs of disjoint homogeneous
  4-sets"), which collapses C1, C2 and C3 into a single certificate. *Status:* this
  instance was attempted (1,558,516 clauses with the hom-4-free-core reduction; 4.4M
  clauses unreduced) and did **not** terminate in ~11 hours with plain CaDiCaL and only
  the vertex-0-prefix symmetry break. It may become feasible with SMS-style dynamic
  symmetry breaking or `satsuma`-style static Johnson-symmetry breaking. **If it lands,
  this is by far the best route** — one LRAT certificate replaces the entire catalogue
  problem.

- **(c) Isomorphism-free SAT enumeration.** Enumerate all (4,4,16) graphs by SAT with
  complete symmetry breaking, blocking each solution. Attempted here with only
  adjacent-transposition lex breaking: 1.195M lex-surviving models found, all in the
  same two isomorphism classes, no termination. Needs *complete* symmetry breaking
  (SMS) to be viable.

**Recommendation:** attempt (b) first with serious symmetry breaking. Fall back to (a)
only if (b) is refractory, and budget for the canonical-form formalisation honestly.

### C3. The two SAT refutations — **do this first**

Required form (one per core):

```lean
lemma core0_unsat : ¬ ∃ x : Fin 64 → Bool, core0_cnf_satisfied x
```

**This obligation is nearly solved already.** Lean 4 core ships a *verified* LRAT
checker as part of `bv_decide` ⚠, and the certificates for both instances are already
in LRAT form (produced via `drat-trim -L`; see `~/z20_repro/drat/core{0,1}.lrat`).

Work required:
1. Define the CNF in Lean over `Fin 64 → Bool` — ideally *generated* from the same
   source as the C generator, so the Lean formula and the checked CNF are the same
   object by construction rather than by inspection.
2. Prove the **reflection lemma**: satisfying the CNF ↔ the graph-theoretic statement
   "this 20-vertex graph has no two disjoint homogeneous 4-sets". This is the part that
   carries real mathematical content and is where an encoding bug would hide. Budget
   most of C3's effort here, not on the checker.
3. Feed the LRAT to the verified checker.

Note `drat-trim` reports **0 RAT lemmas**, so the certificates are pure RUP — the easiest
fragment, and well within what the verified checker handles.

### C4. z(8) ≤ 3 and z(12) ≤ 4

```lean
lemma z_eight_le_three (G : SimpleGraph (Fin 8)) : Cocolourable G 3
lemma z_twelve_le_four (G : SimpleGraph (Fin 12)) : Cocolourable G 4
```

- **z(8) ≤ 3** is the tractable one: 2^28 labelled graphs is too many to `decide`
  naively, but 12,346 up to isomorphism. Either (i) enumerate up to isomorphism —
  which needs the same canonical-form machinery as C2(a), or (ii) find a *human* proof.
  A hand proof may well exist: 8 ≥ R(3,3) = 6 gives a homogeneous triple; iterate.
  **Look for the hand proof before formalising a computation.**

- **z(12) ≤ 4** decomposes as: if `G` has a homogeneous 4-set, use it plus z(8) ≤ 3;
  otherwise `G` is a (4,4)-graph on 12 vertices. The second branch is 1,449,166 graphs.
  Same options as C2. If C2 strategy (a) is built, this reuses it directly.

`★ Design observation.` C2(a) and C4 both need "enumerate all (4,4)-graphs on n vertices
up to isomorphism, verifiably". Building that once, well, discharges most of the
computational content of the whole project. Conversely, if C2(b) succeeds, C4 still
needs it — so the enumeration machinery is probably unavoidable unless a hand proof of
z(12) ≤ 4 can be found.

---

## 5. Milestones

1. **M1** — definitions, L1, L2, the split/glue lemma, and `zmax_twenty` proved *from
   stated hypotheses* for C1–C4. Compiles, `sorry`-free modulo four explicit `axiom`s
   or hypothesis arguments. This is a genuine, honest deliverable and makes the
   remaining work precisely scoped.
2. **M2** — lower bound (L11) complete, including Paley.
3. **M3** — C3 discharged via the verified LRAT checker, including the reflection lemma.
4. **M4** — C1 discharged (or imported from Mathlib).
5. **M5** — C4 discharged.
6. **M6** — C2 discharged; remove all hypotheses; `zmax_twenty` closed.

M1–M3 are, I think, achievable by a competent Lean user in a reasonable time.
M5 and M6 are research-grade formalisation projects.

---

## 6. Honest risk register

| risk | severity | note |
|---|---|---|
| Canonical-form (nauty-equivalent) formalisation for C2(a)/C4 | **high** | plausibly the largest single component |
| Kernel performance on 10⁶-scale enumeration | high | may force `native_decide`, which many reviewers reject |
| Reflection lemma for C3 encoding is subtly wrong | medium | highest-value place to concentrate review |
| Mathlib API drift breaking the skeleton | low | mechanical to fix |
| C2(b) never terminates | medium | it did not here; needs stronger symmetry breaking |

## 7. What exists already

In `~/z20_repro/`: the C orderly generator (`nauty/gen44.c`) and cocolourability
decision procedure (`nauty/cochk.c`); both CNFs and DRUP certificates
(`certificate/`); LRAT translations and a `cake_lpr` build (`cake_lpr/`); independent
CNF regeneration and RUP checker (`verify_certificate.py`); the two core graph6 strings;
and result logs for every computation. These are the *unverified* originals — their role
in a Lean project is as oracles to generate and cross-check the Lean-side objects, not
as trusted inputs.
