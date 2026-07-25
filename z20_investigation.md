# Sorting Twenty Strangers

**The answer is six.** This is an account of how it was found, including seventeen hours spent looking in the wrong place.

## The puzzle

Picture twenty people at a party. Some pairs have met before; most haven't. Draw a dot for each person and a line between two dots whenever those two already know each other. That web of dots and lines is what mathematicians call a *graph* — a map of who is connected to whom.

Now play a sorting game. Divide the twenty into groups under one rule: inside any group, either *everyone* already knows *everyone*, or *nobody* knows *anybody*. A group where two people have met but a third is a stranger to them breaks the rule. Keep making groups until everyone is placed.

Some parties sort easily, some don't. The fewest groups a given party can be sorted into is its *cochromatic number*. The question here is the worst case: across every possible twenty-person party, what is the largest number of groups you could ever be forced into?

This is the first unsolved case of a problem posed by Paul Erdős and John Gimbel around 1990, catalogued as Erdős Problem #758. The answer was known for every party size up to nineteen — the values run 1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6 — and there it stopped. At twenty the answer was known to be either six or seven, and nobody knew which.

## Why you cannot simply check

Twenty people give 190 possible pairs, each either connected or not, so there are 2¹⁹⁰ possible parties. That number is past astronomical: it dwarfs the count of atoms in the observable universe. No computer will ever walk that list.

Checking a single party is not free either. Deciding whether one particular party sorts into six groups is itself a hard combinatorial problem. So the task is a hard problem buried inside an impossibly large pile of them.

## The approach that failed

The natural attack is a contest between two programs. A **Proposer** hunts for a party that *cannot* be sorted into six groups, since finding one would prove the answer is seven. A **Checker** takes each proposed party and tries to sort it. Almost always it succeeds, and every successful sorting is handed back to the Proposer as a lesson: *this party wasn't your counterexample, and here is exactly why*. The Proposer files the lesson away and returns with a party engineered to dodge everything learned so far.

This is a standard and respectable technique. It ran for seventeen hours, reached iteration 63, and accumulated **42.8 million** learned lessons.

It got nowhere, and the diagnostics said so clearly. The natural progress measure is how close the Proposer's best candidate comes to being un-sortable. That measure sat at **43,843** — set at iteration 3 — and never moved again across sixty iterations. The search was not converging. It was circling.

The reason turned out to be more embarrassing than a lack of compute. The Proposer was never *trying* to find a hard party. Its only instruction was to escape the specific lessons already collected, and almost any party does that while remaining trivially sortable. Worse, when the six best candidates it had produced were examined closely, **five of them contained a group of five mutual strangers or five mutual acquaintances** — and any party containing such a group is sortable into six, provably, before any checking begins. Five of the six best results had been outside the space of possible answers all along.

Seventeen hours of computation had been measuring the wrong thing.

## The argument that worked

The answer came instead from an old theorem and a small observation.

The theorem is **Ramsey's**, in the specific form R(4,4) = 18: any party of eighteen or more people contains four who all know each other, or four who are all strangers. Call such a foursome *homogeneous*. Since twenty exceeds eighteen, every party we care about contains at least one.

The observation is about what happens next. Suppose some party contained no *two separate* homogeneous foursomes. Take the one foursome it does have and set those four people aside. The remaining sixteen can then contain no homogeneous foursome at all — if they did, it would be separate from the first. But sixteen-person parties with no homogeneous foursome are extraordinarily rare. **There are exactly two of them.**

That collapses the problem. Any hypothetical hard party must consist of one homogeneous foursome, plus one of exactly two known sixteen-person cores, plus some pattern of connections between them — and there are only 4 × 16 = **64** such connections to decide. The search space drops from 2¹⁹⁰ to two problems of size 2⁶⁴, which for a SAT solver is nothing.

Both came back **unsatisfiable**, in **1,571** and **789** decision steps — under a second of computation. No such party exists. Therefore every twenty-person party contains two separate homogeneous foursomes.

The rest is arithmetic. Take those two foursomes as two groups. Eight people are placed, twelve remain, and twelve-person parties are known to sort into four groups. Two plus four is six. So **every** twenty-person party sorts into six groups.

Six is also forced, not merely sufficient. The Paley graph on seventeen vertices — a classical object built from squares modulo 17 — has the property that no four of its vertices are mutually connected and no four are mutually unconnected. Every group in any sorting of it therefore holds at most three people, so seventeen people need at least ⌈17/3⌉ = six groups. Pad it with three extra people and you have a twenty-person party still requiring six.

Six achievable, six unavoidable. **z(20) = 6.**

## Checking it

A computer-assisted proof is only as good as its weakest unchecked assumption, and this one had several. Each was closed.

The two sixteen-person cores were taken on faith from a published catalogue. So the catalogue was regenerated from scratch — building every party with no homogeneous foursome, size by size, from one person up. The counts came out 1, 2, 4, 9, 24, 84, 362, 2,079, 14,701, 103,706, 546,356, 1,449,166, 1,184,231, 130,816, 640, **2**, 1, **0**. Exactly two at sixteen, matching the catalogue character for character. One at seventeen, which is the Paley graph. And zero at eighteen — which re-derives R(4,4) = 18 independently, a useful sign the machinery is sound, since any other answer there would have contradicted a classical theorem.

The claim that twelve-person parties sort into four groups came from a separate published computation. It was re-derived here too: every party of eight people sorts into three groups (all **12,346** of them, checked exhaustively), and every twelve-person party with no homogeneous foursome sorts into four (all **1,449,166**, checked exhaustively). Those two cases are exhaustive, so the claim holds. This route is stronger than the historical one, which went through chromatic numbers and had a genuine exception needing a separate hand-check.

The two unsatisfiability results were confirmed by three independent checkers — a hand-written one, the standard `drat-trim`, and **`cake_lpr`, whose checking core is formally verified** — each run against proof formulas regenerated independently rather than the originals, and each with deliberate negative controls confirming the checks could actually fail when given a wrong proof.

What remains unchecked is now narrow and mundane: the correctness of two small programs written for this purpose, both cross-validated against known results, and one format-translation step sitting between the original proof and the verified checker.

## What the failure was worth

The contrast is stark enough to be worth stating plainly. The search approach consumed roughly forty-five CPU-hours across four parallel formulations and produced no result. The structural approach produced a complete answer in under a second.

The difference was not speed. It was that the search was asked to explore 2¹⁹⁰ possibilities while knowing nothing about their structure, and the reduction used a theorem from 1935 to prove that all but two of them were irrelevant. Ramsey's theorem was available the entire time. Nothing prevented the search from discovering the same structure on its own except that it had no reason to look, and no way to recognise it if it had.

There is a general lesson in that, and it is not about hardware. When a search stalls, the productive question is rarely *how do I search harder*. It is *what do I already know that would make this search unnecessary*.

---

# Technical appendix

Terminology below drops the party metaphor: *graph*, *vertex*, *edge*, *clique*, *independent set*. A vertex set is **homogeneous** if it induces a clique or an independent set. `hom4`/`hom5` denote homogeneous 4-sets and 5-sets.

## A. Statement

The **cochromatic number** z(G) is the minimum number of classes in a partition of V(G) with every class homogeneous. Define z(n) = max{z(G) : |V(G)| = n}. Published values: z(1..19) = 1,1,2,2,3,3,3,3,4,4,4,4,5,5,5,6,6,6,6; z(20) was open, known to be 6 or 7 (Erdős Problem #758).

**Result: z(20) = 6.**

## B. The proof

**Upper bound.** Let G be any graph on 20 vertices.

1. 20 ≥ R(4,4) = 18, so G contains a homogeneous 4-set A.
2. Relabel A = {0,1,2,3}. If A is independent, complement G — the property "has two disjoint homogeneous 4-sets" is complement-invariant, since complementation preserves the family of homogeneous sets setwise. So WLOG A is a clique.
3. If V∖A contains a homogeneous 4-set, it is disjoint from A and we are done. Otherwise G[V∖A] is a 16-vertex graph with no homogeneous 4-set, i.e. a (4,4)-Ramsey graph, of which there are exactly two up to isomorphism (§F).
4. For each core, the 64 cross-edge variables are decided by SAT: **both instances are UNSAT** (§D, §E). Hence case 3's "otherwise" is impossible.
5. Therefore every 20-vertex graph has two *disjoint* homogeneous 4-sets A, B. Take them as two classes; the remaining 12 vertices need at most z(12) ≤ 4 (§G). Total ≤ 6, refinable to exactly 6 since n ≥ 6. So **z(20) ≤ 6**.

**Lower bound (no computation needed).** Paley(17) is edge-transitive, so a hypothetical K₄ may be assumed to contain {0,1}; the common neighbours of 0 and 1 are {2,9,16}, with pairwise differences 7 and 14 — neither a quadratic residue — so they are pairwise non-adjacent and no K₄ exists. Self-complementarity (multiply by a non-residue) rules out an independent 4-set. Hence every homogeneous set has ≤ 3 vertices and ⌈17/3⌉ = 6 classes are needed; monotonicity under induced subgraphs lifts this to Paley(17)+3K₁ on 20 vertices. An explicit six-class partition (§H) shows the value is exactly 6. So **z(20) ≥ 6**, by hand.

**Hence z(20) = 6.** ∎

## C. A useful equivalence (not needed above, but clarifying)

c₆(G) = 0 ⟺ G has no hom5 **and** no two disjoint hom4s.

*(⇐)* A 6-class partition of 20 satisfies Σ(sᵢ−3) = 2, so some class has size ≥ 4; if all are ≤ 4 then at least two have size exactly 4. *(⇒)* If a hom5 exists, use it as a class and cocolour the other 15 with z(15) = 5. If two disjoint hom4s exist, use them and cocolour the other 12 with z(12) = 4. Either way c₆ > 0.

Exhaustive check: of the 90 six-class shapes of 20, zero have all classes ≤ 3, and zero have max ≤ 4 with fewer than two 4s. The four admissible hom5-free shapes are (3,3,3,3,4,4), (2,3,3,4,4,4), (2,2,4,4,4,4), (1,3,4,4,4,4).

## D. The two SAT instances

Variables: 64 cross edges, `cross_var(a,b) = 1 + 16a + b` for anchor a ∈ {0..3}, core b ∈ {0..15}. A is a fixed clique; the core is fixed to one of the two Ramsey graphs. No hom4 lies wholly inside A (it *is* A, and everything disjoint from A lies in the core, which is hom4-free), so only *mixed* homogeneous 4-sets matter. These number **872** per core:

| split | condition | count |
|---|---|---|
| 3 in A + 1 in core | clique; 3 cross edges present | 64 |
| 2 in A + 2 in core | clique; core pair is an edge; 4 cross edges | 6 × 60 = 360 |
| 1 in A + 3 in core | clique over a core triangle | 4 × 56 = 224 |
| 1 in A + 3 in core | independent over a core independent triple | 4 × 56 = 224 |

For every vertex-disjoint pair of conditions, one clause negates the conjunction of both. That gives **104,524** clauses per core, lengths {6: 43,840, 7: 52,416, 8: 8,268}. Solved by a clause-learning-free DPLL emitting a blocking clause per refuted cube: UNSAT in **1,571** and **789** nodes.

## E. Verification of the refutations

Performed without executing any of the certificate package's code (its generator was read only to learn the variable convention).

| check | result |
|---|---|
| CNFs regenerated by an independent generator | clause **sets identical**, same length histogram |
| semantic check: 300 random assignments/core | CNF satisfied ⟺ the 20-vertex graph has no two disjoint hom4s — **300/300** |
| own RUP checker vs **my** CNFs | 1,571 / 789 steps, empty clause derived |
| `drat-trim` vs my CNFs | **s VERIFIED**, 0 RAT lemmas (pure RUP) |
| `cake_lpr` (formally verified core) vs my CNFs, via `drat-trim -L` → LRAT | **s VERIFIED UNSAT** |
| negative controls: cross-core, empty formula, truncated proof, injected clause | all correctly **rejected** by every checker |

`drat-trim` reported identical proof statistics against the original CNFs and mine (core 0: 1,467/1,572 lemmas, 11,694 resolution steps; core 1: 752/790, 5,705), confirming they are the same formula. `cake_lpr_arm8.S` matched its upstream sha256; `basis_ffi.c` did not, but that file is a C I/O shim outside the CakeML verified boundary and it and the manifest were last touched in the same upstream commit, indicating a stale manifest.

## F. Independent generation of the Ramsey cores

Orderly generation by vertex extension, with nauty `densenauty` canonical forms (`gen44.c`). Completeness holds because every induced subgraph of a (4,4)-graph is a (4,4)-graph, so every level-(n+1) class arises from some level-n class.

Admissibility: adding v with N(v) = S preserves hom4-freeness iff G[S] is triangle-free and G[V∖S] has no independent triple. With ω, α ≤ 3 and R(3,4) = 9 this forces n−8 ≤ |S| ≤ 8.

```
n :  1  2  3  4  5  6   7    8     9     10      11       12       13     14   15 16 17 18
# :  1  2  4  9 24 84 362 2079 14701 103706  546356  1449166  1184231 130816 640  2  1  0
```

n = 16 yields exactly two graphs, identical to McKay's `r44_16.g6` (`OsHHirKdlp[IFVI|KpqfR`, `Ov?IXZIhlRWjUXL[iphst`; m = 60, degrees 7⁸8⁸, 56 triangles, 56 independent triples, hom4 = 0). n = 17 yields one, verified isomorphic to Paley(17). n = 18 yields zero, **re-deriving R(4,4) = 18**.

## G. z(12) ≤ 4, re-derived

Two exhaustive cases, via `cochk` (exact recursive homogeneous-block partition):

- G has a hom4 → that class plus z(8) ≤ 3 on the other 8. Verified: `geng -q 8 | cochk 3` → **12,346 graphs, 0 not 3-cocolourable** (every graph on 8 vertices).
- G has none → G is a (4,4,12) graph. Verified: `gen44d 12 12 | cochk 4` → **1,449,166 graphs, 0 not 4-cocolourable**.

Exhaustive, so z(12) ≤ 4. This avoids the historical chromatic-number argument, which has an exception (a unique 12-vertex graph with χ(G), χ(Ḡ) ≥ 5) requiring separate treatment.

## H. Lower-bound witnesses

| graph | 5-cocolourable? | 6-cocolourable? | conclusion |
|---|---|---|---|
| Paley(17), n=17 | **no** | yes | z(17) = 6 |
| Paley(17) + 2 isolated, n=19 | **no** | yes | z(19) ≥ 6 |
| Paley(17) + 3 isolated, n=20 | **no** | yes | **z(20) ≥ 6** |

## I. Reproduction

Bundle at `~/z20_repro/`:

- `nauty/gen44.c`, `gen44d.c` — orderly generation (needs nauty ≥ 2.9; `cc -O3 -I<nauty> -lnauty`)
- `nauty/cochk.c` — k-cocolourability decision from graph6 on stdin
- `certificate/` — the two CNFs, two DRUP proofs, manifest
- `verify_certificate.py` — independent CNF regeneration, semantic check, own RUP checker
- `drat/` — drat-trim source/binary, my regenerated CNFs, LRAT files
- `cake_lpr/` — formally verified checker (built from `cake_lpr_arm8.S`), LRAT inputs
- `c6_fast.py` — exact c₆ counter (memoized subset DP; ~1.3 s vs ~34 min for enumerate-then-count)
- result files: `gen44_result.txt`, `z12_result.txt`, `lower_bound_result.txt`

External inputs to the final proof: **none**. R(4,4) = 18, the core catalogue, z(8) ≤ 3, z(12) ≤ 4 and the lower bound were all re-derived here.

## J. Post-mortem on the CEGIS run

The abandoned search is preserved (checkpointed at iteration 63, 42.8M clauses, `RESUME.md`) because its failure mode is instructive.

- **Objective mismatch.** The outer solver minimised nothing. It sought any graph escaping the accumulated blocking clauses, which is nearly orthogonal to seeking a graph with few cocolourings.
- **The progress metric was invalid.** The running minimum of exhaustively-counted candidates was flat at 43,843 from iteration 3 onward. Five of the six best candidates contained a hom5 and so were provably 6-cocolourable by z(15) = 5 — outside the witness space entirely.
- **A constraint was missing.** Adding ω ≤ 4 and α ≤ 4 costs 2·C(20,5) = 31,008 clauses, is sound and complete by that same lemma, kills ~40 bits of entropy, and bounds every block to size ≤ 4 (collapsing the block universe to C(20,3)+C(20,4) = 5,985).
- **Baselines were wrong.** A working assumption that a random 20-vertex graph has ≈1.376M six-cocolourings was retired: the measured mean over exhaustively counted samples is **1,032,370**, with enormous spread (0.32M–1.79M).
- **A cheap alternative existed.** A hill-climb over the 54 padding bits of Paley(17)+3, using exact c₆ as the objective, reached c₆ = 7,041 in about two minutes — 6.2× below the CEGIS floor that cost 17 hours. Even its *random starting point* beat that floor by 2.2×.
- **Hardware was never the constraint.** A second solver seed was attempted and had to be killed: two instances on a 16 GB machine drove 25 GB of swap and starved the incumbent to 1.5% CPU, making combined progress worse than one solver alone.
