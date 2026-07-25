# The cochromatic number of graphs on twenty vertices: z(20) = 6

**Status: candidate computer-assisted proof, offered for independent scrutiny.**

## Abstract

Let z(G) denote the cochromatic number of a graph G — the least number of classes in a
partition of V(G) in which every class induces a clique or an independent set — and let
z(n) = max{z(G) : |V(G)| = n}. The values z(1),…,z(19) are known; z(20) was open, with
6 ≤ z(20) ≤ 7 (Erdős Problem #758). We prove **z(20) = 6**.

The upper bound reduces to two propositional instances of 64 variables each, both
unsatisfiable, via the observation that a 20-vertex graph without two vertex-disjoint
homogeneous 4-sets would contain a 16-vertex Ramsey (4,4)-graph, of which there are exactly
two. All inputs — R(4,4) = 18, the completeness of the 16-vertex catalogue, z(8) ≤ 3,
z(12) ≤ 4, and the lower bound — were recomputed independently; the two refutations were
checked by three independent proof checkers, one of them formally verified.

## 1. Notation

A vertex set is **homogeneous** in G if it induces a clique or an independent set; a
**cocolouring** is a partition of V(G) into homogeneous classes; z(G) is the least number of
classes in such a partition. We write *hom-k* for a homogeneous set of size k. A
**(4,4)-graph** is a graph with no hom-4, i.e. containing neither K₄ nor an independent
4-set. R(4,4) = 18 is the classical Ramsey number.

Two elementary facts are used without further comment.

**(N1)** z is monotone under induced subgraphs: if H is an induced subgraph of G, then
z(H) ≤ z(G), since restricting a cocolouring of G to V(H) yields a cocolouring of H with no
more classes (an induced subgraph of a homogeneous set is homogeneous).

**(N2)** The family of homogeneous sets is preserved setwise under complementation, since
complementation exchanges cliques and independent sets. Hence any property defined purely in
terms of the homogeneous-set family — in particular "possesses two disjoint hom-4s" — is
complement-invariant.

## 2. Result

> **Theorem.** z(20) = 6.

## 3. The upper bound

> **Lemma 3.1.** Every graph on 20 vertices contains two vertex-disjoint homogeneous 4-sets.

*Proof.* Let G have 20 vertices. Since 20 ≥ R(4,4) = 18, G contains a hom-4, say A.
By (N2) we may complement G if necessary, so assume A is a clique, and relabel A = {0,1,2,3}.
Put B = V(G) ∖ A, so |B| = 16.

If G[B] contains a hom-4, that set is disjoint from A and the lemma holds. So assume G[B]
contains none; then G[B] is a (4,4)-graph on 16 vertices. By Lemma 4.1 there are exactly two
such graphs up to isomorphism, namely

```
C0 = OsHHirKdlp[IFVI|KpqfR
C1 = Ov?IXZIhlRWjUXL[iphst
```

(graph6; both have 60 edges, degree sequence 7⁸8⁸, 56 triangles, 56 independent triples).

Fix G[B] to be C₀ or C₁. The only remaining freedom is the 4 × 16 = 64 edges between A and B.
Now observe which sets can be hom-4s in G:

- a hom-4 inside B: none, since G[B] is a (4,4)-graph;
- A itself: a clique, but every *mixed* set meets A, and every set disjoint from A lies in B;
- **mixed** sets, with 1–3 vertices in A: these are the only candidates for a disjoint pair.

Enumerating the mixed sets that *can* be homogeneous, given that A is a clique and G[B] is
fixed, gives exactly 872 conditions per core (§5). For each vertex-disjoint pair of such
conditions we assert that they do not both hold. This yields a CNF over the 64 cross-edge
variables with 104 524 clauses, whose satisfying assignments are precisely the graphs G of
the assumed form possessing no two disjoint hom-4s.

Both instances (one per core) are **unsatisfiable** (§6). Hence no such G exists, and the
assumption that G[B] contains no hom-4 is untenable. ∎

> **Lemma 3.2.** z(12) ≤ 4.

*Proof (computational, §7).* Let G have 12 vertices. If G has a hom-4 A, take A as one class;
the remaining 8 vertices need at most z(8) ≤ 3 classes, giving 4. If G has no hom-4, then G
is a (4,4)-graph on 12 vertices. Both z(8) ≤ 3 and the 4-cocolourability of every
(4,4)-graph on 12 vertices were verified exhaustively (§7). The two cases are exhaustive. ∎

> **Proposition 3.3.** z(20) ≤ 6.

*Proof.* Let G have 20 vertices. By Lemma 3.1 pick disjoint hom-4s A, B and take them as two
classes. The remaining 12 vertices induce a graph cocolourable in at most z(12) ≤ 4 classes
by Lemma 3.2. This gives a cocolouring with at most 6 classes; since |V(G)| = 20 ≥ 6, any
cocolouring with fewer than 6 classes may be refined to exactly 6 by splitting a class
(a subset of a homogeneous set is homogeneous). ∎

## 4. The 16-vertex catalogue

> **Lemma 4.1.** Up to isomorphism there are exactly two (4,4)-graphs on 16 vertices.

This is due to McKay (`r44_16.g6`). We recomputed it independently by orderly generation
(§8). The generation also yields the whole sequence of (4,4)-graph counts and, at n = 18,
re-derives R(4,4) = 18:

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| # | 1 | 2 | 4 | 9 | 24 | 84 | 362 | 2079 | 14701 | 103706 | 546356 | 1449166 | 1184231 | 130816 | 640 | **2** | 1 | **0** |

The two graphs at n = 16 agree with McKay's file character for character; the unique graph at
n = 17 was verified isomorphic to the Paley graph of order 17.

## 5. The propositional encoding

Variables x_{a,b} (a ∈ A, b ∈ B) for the 64 cross edges. With A a clique and G[B] fixed and
hom-4-free, a mixed set is homogeneous exactly in these cases:

| split | requirement | count |
|---|---|---|
| 3 in A, 1 in B | clique: the 3 cross edges present | 4 · 16 = 64 |
| 2 in A, 2 in B | clique: the B-pair is an edge, 4 cross edges present | 6 · 60 = 360 |
| 1 in A, 3 in B | clique over a triangle of G[B]: 3 cross edges present | 4 · 56 = 224 |
| 1 in A, 3 in B | independent over an independent triple of G[B]: 3 cross edges absent | 4 · 56 = 224 |
| | **total** | **872** |

Each condition is a conjunction of 3 or 4 cross-edge literals. For each of the vertex-disjoint
pairs of conditions we add the clause negating the conjunction of both, giving 104 524 clauses
of lengths {6: 43 840, 7: 52 416, 8: 8 268}. The projection onto the cross-edge variables is
exact: an assignment satisfies the CNF iff the corresponding G has no two disjoint hom-4s.

## 6. Verification of the two refutations

Both instances were refuted by a DPLL search without clause learning, emitting one blocking
clause per refuted cube (1 571 and 789 lines respectively). Verification was carried out
against CNFs **regenerated independently** from the graph6 strings, not against the original
files:

| check | core 0 | core 1 |
|---|---|---|
| independent CNF regeneration (clause sets) | identical | identical |
| semantic test, 300 random assignments each | 300/300 | 300/300 |
| independent RUP checker | verified | verified |
| `drat-trim` | `s VERIFIED` | `s VERIFIED` |
| `cake_lpr` (formally verified core), via LRAT | `s VERIFIED UNSAT` | `s VERIFIED UNSAT` |

The semantic test compares CNF satisfaction against a direct computation of "has two disjoint
hom-4s" on the full 20-vertex graph, confirming the encoding means what §5 claims. Negative
controls (cross-core proof/CNF pairings, empty formula, truncated proof, injected clause) were
correctly rejected by every checker. `drat-trim` reported 0 RAT lemmas, so the certificates lie
in the RUP fragment.

## 7. z(8) ≤ 3 and z(12) ≤ 4

Both by exhaustive enumeration, using an exact cocolourability decision procedure:

- **z(8) ≤ 3:** all 12 346 graphs on 8 vertices (generated by `geng`) are 3-cocolourable.
- **(4,4)-graphs on 12 vertices:** all 1 449 166 are 4-cocolourable.

With the case split of Lemma 3.2 these are exhaustive. We note this route avoids the
chromatic-number formulation used previously for z(12), which admits an exception (a unique
12-vertex graph with χ(G), χ(Ḡ) ≥ 5) requiring separate treatment.

## 8. The lower bound

> **Proposition 8.1.** z(20) ≥ 6.

*Proof.* Let P be the Paley graph of order 17 (vertices Z_17, i ~ j iff i - j is a nonzero
quadratic residue mod 17; residues {1,2,4,8,9,13,15,16}).

P has no K_4. The affine maps x -> ax+b with a a quadratic residue act transitively on
edges (note -1 = 16 is a residue, so x -> -x+1 swaps 0 and 1), so a hypothetical K_4 may be
assumed to contain the edge {0,1}. The common neighbours of 0 and 1 are
Q ∩ (1+Q) = {2, 9, 16}, whose pairwise differences are 7 and 14 — neither a quadratic
residue. So those three are pairwise non-adjacent, and no two of them can complete {0,1} to
a K_4. Multiplication by a non-residue (e.g. 3) is an isomorphism P -> P-complement, so P
has no independent 4-set either.

Hence every homogeneous set of P has at most 3 vertices, and any cocolouring of P needs at
least ceil(17/3) = 6 classes. Let G be P together with three isolated vertices, a graph on
20 vertices containing P as an induced subgraph. By (N1), z(G) >= z(P) >= 6. ∎

An explicit six-class cocolouring of G shows the value is exactly 6 (vertices 17,18,19
isolated):

    I1 = {0,3,6,17,18,19}   I2 = {1,4,7}      I3 = {2,9,12}
    I4 = {5,8,11}           I5 = {10,13,16}   K1 = {14,15}

The first five classes are independent and the last is an edge; together they cover all 20
vertices exactly once. The lower bound therefore requires no solver.

Propositions 3.3 and 8.1 give the Theorem. ∎

## 9. Dependencies

No *mathematical* input is taken on trust: each of the following was recomputed here
rather than cited. This is not the same as verifying the trusted computing base —
see the caveat after the table.

| input | how obtained |
|---|---|
| R(4,4) = 18 | orderly generation; no (4,4)-graph on 18 vertices |
| exactly two (4,4)-graphs on 16 vertices | orderly generation (Lemma 4.1) |
| z(8) ≤ 3 | exhaustive, 12 346 graphs |
| z(12) ≤ 4 | Lemma 3.2, exhaustive |
| two refutations | three independent checkers, one formally verified |
| z(20) ≥ 6 | Proposition 8.1, verified computationally |

**What this does and does not establish.** `drat-trim` and `cake_lpr` certify the SAT
layer: that the CNFs supplied to them are unsatisfiable. They do not establish that the
graph-to-CNF translation has the stated semantics, nor that the generator enumerates every
isomorphism class, nor that the cocolourability procedure searches exhaustively. Those
encoding lemmas are supported by semantic spot-testing and by differential validation
against published data, not proved; a correlated implementation error remains logically
possible. The accurate description is *a complete, locally regenerated computer-assisted
proof with independently checked SAT refutations*.

What remains unverified is the correctness of two purpose-written programs — the orderly
generator and the cocolourability decision procedure — and the DRUP→LRAT translation step
preceding the formally verified checker. The generator is cross-validated by reproducing the
published (4,4)-graph counts and re-deriving R(4,4) = 18; the decision procedure is
cross-validated against known z values.

## 10. Reproduction

Artifacts (source, certificates, checkers, results) are available and comprise: the orderly
generator (C, requiring nauty ≥ 2.9); the cocolourability decision procedure (C, reading
graph6); the two CNFs and DRUP certificates; an independent CNF regenerator and RUP checker;
LRAT translations and the `cake_lpr` build; and result logs for each computation above.

## 11. Provenance

Every mathematical step below was produced by AI systems. The human participant selected the
problem and mediated between systems; he makes no claim to the mathematics. The division of
labour is set out in full so that readers can weight the result accordingly.

**Phase 1 — the approach that failed.** A locally run Nous Hermes agent designed a CEGIS
harness — an outer SAT solver proposing candidate graphs, an inner verifier refuting them with
harvested cocolourings — and drove OpenAI's GPT-5.6 Sol within it. This ran for roughly two
days and accumulated about 42 million learned clauses without resolving the problem. It appears
here only as a documented failure mode (§J of the accompanying essay): the outer solver
minimised nothing relevant, and its apparent progress metric was later shown to be invalid,
five of its six best candidates being provably 6-cocolourable before any checking.

**Phase 2 — intermediate analysis.** Anthropic's Claude 4.8 worked on the harness output:
instrumentation, baseline measurements, and the statistical characterisation of the candidate
graphs the search was producing.

**Phase 3 — the reduction.** GPT-5.6 Sol, contributing directly rather than through the
harness, produced the structural reduction that settles the question — that a 20-vertex graph
without two disjoint hom-4s must contain one of exactly two 16-vertex Ramsey graphs, collapsing
the search to two 64-variable instances — together with the CNF generator, the DPLL solver and
the DRUP certificates. Contributing models also supplied the equivalence of §C and the
diagnosis that Phase 1's progress metric was measuring the wrong quantity.

**Phase 4 — verification.** Anthropic's Claude Opus 5 carried out the independent verification
of §6, the recomputation of the 16-vertex catalogue and of R(4,4) = 18 in §4, the re-derivation
of z(8) ≤ 3 and z(12) ≤ 4 in §7, the lower-bound construction of §8, and this write-up.

No step of the final argument rests on an assertion by a language model that was not
subsequently recomputed from first principles by a different system than the one that asserted
it. The result should be treated as a candidate proof pending independent scrutiny.
