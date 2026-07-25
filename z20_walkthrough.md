---
title: "Understanding the proof that $z(20) = 6$"
subtitle: "A walkthrough of the cochromatic number of 20-vertex graphs (Erdős Problem \\#758)"
date: "25 July 2026"
geometry: margin=2.6cm
fontsize: 11pt
mainfont: "Palatino"
colorlinks: true
toc: true
toc-depth: 2
---

\newpage

# Part 1: What we are proving

**Cochromatic number.** For a graph $G$, a *cocolouring* splits the vertices into groups
where each group is either a **clique** (everyone joined) or an **independent set** (nobody
joined). Call such a group *homogeneous*. Then $z(G)$ is the fewest groups you need.

Quick sanity check: a 5-cycle. Any three of its vertices contain both an edge and a
non-edge, so every homogeneous set has size at most 2 --- you need at least
$\lceil 5/2 \rceil = 3$ groups, and 3 works. So $z(C_5) = 3$.

**The quantity we want** is
$$z(20) \;=\; \max\{\, z(G) : G \text{ a graph on } 20 \text{ vertices} \,\}.$$

That "max" means the proof splits in two, and both halves are genuinely needed:

| | what it says | how you prove it |
|---|---|---|
| $z(20) \le 6$ | *every* 20-vertex graph needs at most 6 | a universal claim --- hard |
| $z(20) \ge 6$ | *some* 20-vertex graph needs 6 | exhibit one graph --- easy |

> **Insight.** The asymmetry is the whole story. Lower bounds on a maximum are cheap:
> produce one example. Upper bounds are expensive: rule out $2^{190}$ possibilities.
> Almost all the machinery goes into the $\le$ direction.

# Part 2: The lower bound (the easy half)

We need one 20-vertex graph that genuinely cannot be done in 5 groups.

**The Paley graph on 17 vertices.** Vertices are $0,\dots,16$. Join $i$ and $j$ when
$i - j$ is a **quadratic residue** mod 17 --- a nonzero perfect square mod 17. Those are
$\{1, 2, 4, 8, 9, 13, 15, 16\}$.

The property that matters: **its largest clique is 3, and its largest independent set is 3.**

This is provable by hand, and worth seeing. The maps $x \mapsto ax+b$ with $a$ a residue act
transitively on edges (note $-1 \equiv 16$ is a residue, so $x \mapsto -x+1$ swaps 0 and 1),
so any hypothetical $K_4$ may be assumed to contain the edge $\{0,1\}$. The common
neighbours of 0 and 1 are $Q \cap (1+Q) = \{2, 9, 16\}$, and their pairwise differences are
7 and 14 --- neither a quadratic residue. So those three are pairwise non-adjacent, and no
two can complete $\{0,1\}$ to a $K_4$. Multiplying by a non-residue is an isomorphism to the
complement, so there is no independent 4-set either.

Now the pigeonhole. Every homogeneous set has at most 3 vertices. To cover 17 vertices
with groups of size at most 3 you need at least $\lceil 17/3 \rceil = 6$ groups. So
$z(\mathrm{Paley}(17)) \ge 6$.

**Getting from 17 to 20.** Add three isolated vertices. Why does that not help? Because
of a general fact:

> If $H$ sits inside $G$ as an induced subgraph, then $z(H) \le z(G)$.

*Why:* take any cocolouring of $G$ and delete the vertices not in $H$. Each group shrinks,
and a subset of a clique is still a clique, a subset of an independent set still
independent. So you get a valid cocolouring of $H$ with no more groups.

So our 20-vertex graph contains Paley(17), hence needs at least 6. **$z(20) \ge 6$.**

And here is an explicit six-class cocolouring, so the value is exactly 6 (vertices
$17,18,19$ isolated):
$$
\begin{aligned}
I_1 &= \{0,3,6,17,18,19\} & I_2 &= \{1,4,7\} & I_3 &= \{2,9,12\} \\
I_4 &= \{5,8,11\} & I_5 &= \{10,13,16\} & K_1 &= \{14,15\}
\end{aligned}
$$
The first five are independent, the last is an edge. **The entire lower bound is therefore
hand-checkable** --- no solver is involved at any point.

# Part 3: The upper bound --- the target

We must show *every* 20-vertex graph $G$ can be done in 6.

**The strategy is subtraction.** Suppose we could always find **two disjoint homogeneous
4-sets** $A$ and $B$ in $G$. Make them two groups. That uses 8 vertices and 2 groups. The
remaining 12 vertices form some graph, and if every 12-vertex graph needs at most 4 groups,
we are done:
$$2 \text{ groups} + 4 \text{ groups} = 6 \text{ groups}.$$

So the upper bound reduces to two claims:

- **(I)** Every 20-vertex graph contains two disjoint homogeneous 4-sets.
- **(II)** $z(12) \le 4$.

> **Insight.** Notice what just happened: we replaced "partition 20 vertices into 6
> homogeneous classes" --- a statement about the whole structure --- with "find two
> disjoint 4-sets". Two 4-sets is a much smaller object to hunt for. This is the move that
> makes everything else possible, and it is why an earlier 17-hour search failed: it was
> searching over *partitions* when it should have been reasoning about *4-sets*.

# Part 4: Claim (I) --- the heart of it

**Step 1 --- one 4-set is free.** Ramsey's theorem says $R(4,4) = 18$: any graph on 18 or
more vertices contains 4 mutual friends or 4 mutual strangers. Since $20 \ge 18$, our $G$
contains at least one homogeneous 4-set. Call it $A$.

**Step 2 --- assume $A$ is a clique, without loss of generality.** $A$ might be an
independent set instead. If so, flip $G$ to its complement. Under complementation cliques
become independent sets and vice versa, so *homogeneous sets are exactly preserved*, and so
is the property "has two disjoint homogeneous 4-sets". Relabel so $A = \{0,1,2,3\}$.
(Part 9 examines this step in detail.)

**Step 3 --- the collapse.** Suppose, for contradiction, that $G$ has **no** two disjoint
homogeneous 4-sets. Look at the other 16 vertices, call them $B$.

$B$ cannot contain a homogeneous 4-set --- any such set would live entirely in $B$, hence
be disjoint from $A$, giving us the two disjoint sets we assumed do not exist.

So $G[B]$ is a 16-vertex graph with no $K_4$ and no independent 4-set. These are extremely
rare objects, and this is the punchline:

> **There are exactly two such graphs, up to isomorphism.**

**Step 4 --- what is left to decide.** So $G$ must look like: the clique $A$ on 4 vertices,
one of exactly 2 fixed graphs on $B$, and then the $4 \times 16 = 64$ edges between them.
Everything else is pinned down. Two problems of $2^{64}$ each --- small enough to settle
exhaustively.

**Step 5 --- the computation.** For each of the two cores we ask a SAT solver: *is there
any way to wire the 64 cross edges so that no two disjoint homogeneous 4-sets appear?*
Both answers: **no** (unsatisfiable).

Therefore Step 3's assumption was false. **Every 20-vertex graph has two disjoint
homogeneous 4-sets.**

# Part 5: Claim (II) --- $z(12) \le 4$

Same shape of argument, one size down. Let $G$ have 12 vertices.

- **If $G$ has a homogeneous 4-set:** use it as one group. The remaining 8 vertices need at
  most $z(8) \le 3$ groups. Total 4.
- **If $G$ has none:** then $G$ is a hom-4-free graph on 12 vertices. There are
  $1{,}449{,}166$ of these. Every single one was checked to be 4-cocolourable.

The cases are exhaustive, so $z(12) \le 4$. And $z(8) \le 3$ was checked over all
$12{,}346$ graphs on 8 vertices --- every graph, not a sample.

# Part 6: Putting it together

$$
\underbrace{\text{Ramsey}}_{\text{one 4-set}} \to
\underbrace{\text{complement}}_{A \text{ is a clique}} \to
\underbrace{\text{2 cores}}_{B \text{ pinned down}} \to
\underbrace{\text{2 UNSATs}}_{\text{two disjoint 4-sets}} \to
\underbrace{2 + z(12){=}4}_{z(20) \le 6}
$$

together with $z(20) \ge 6$ from Paley(17), gives $\boxed{z(20) = 6}$.

\newpage

# Part 7: Where a sceptic should push

The load-bearing joints, and how each was addressed:

1. **"Exactly two 16-vertex cores"** --- a catalogue claim. Regenerated independently
   (Part 11); the level counts matched published values and level 18 came out empty,
   re-deriving $R(4,4) = 18$.
2. **The SAT encoding** --- does it really capture "no two disjoint hom-4s"? Tested by
   generating 300 random cross-edge assignments per core, building the actual 20-vertex
   graph, computing directly whether it has two disjoint hom-4s, and confirming agreement
   with CNF satisfaction. 300/300 both times.
3. **The refutations** --- checked by three independent checkers (a hand-written RUP
   checker, `drat-trim`, and `cake_lpr` whose core is formally verified), against CNFs
   regenerated from scratch, with deliberate wrong-proof controls that all correctly failed.
4. **$z(12) \le 4$ and $z(8) \le 3$** --- exhaustive, not sampled.
5. **The trusted remainder.** The proof checkers certify the *SAT layer* --- that the CNFs
   given to them are unsatisfiable. They do not certify that the graph-to-CNF translation
   has the stated semantics, that the generator enumerates every isomorphism class, or that
   the cocolourability procedure searches exhaustively. Those encoding lemmas are supported
   by semantic spot-testing and by differential validation against published data, not
   proved. A correlated implementation error remains logically possible.

# Part 8: The complement step --- why the WLOG is free

This is the move that feels like sleight of hand, so let us be precise.

We are proving a statement of the form $\forall G.\ P(G)$, where
$$P(G) = \text{``$G$ has two disjoint homogeneous 4-sets''}.$$

**The key fact:** complementing a graph does not change which sets are homogeneous. A
clique in $G$ becomes an independent set in $\bar{G}$, and vice versa --- but "homogeneous"
means *clique or independent set*, so the collection of homogeneous sets is literally
identical. Therefore
$$P(G) \iff P(\bar{G}).$$

**The argument.** Take an arbitrary $G$. Ramsey hands us a homogeneous 4-set $A$. Two cases:

- $A$ is a clique in $G$: run the main argument on $G$.
- $A$ is independent in $G$: then $A$ is a **clique in $\bar{G}$**. Run the main argument on
  $\bar{G}$ to get $P(\bar{G})$. Since $P(\bar{G}) \iff P(G)$, we have proved $P(G)$ anyway.

So we never lose generality. The relabelling to $A = \{0,1,2,3\}$ is free for the same
reason: $P$ is isomorphism-invariant.

> **Insight.** The WLOG is licensed by an invariance of *the property being proved*, not by
> a symmetry of some particular graph. That is the general test: a "WLOG by complementation"
> is valid exactly when your target property is complement-invariant. Had we been proving
> something about edge counts, the same move would be illegal.

\newpage

# Part 9: The SAT encoding, built by hand

Let us construct actual conditions and an actual clause, so you can see there is no magic.

**Setup.** $A = \{a_0,a_1,a_2,a_3\}$ is a clique. $B = \{b_0,\dots,b_{15}\}$ carries one of
the two fixed cores. The 64 variables are
$$x[i][j] = \text{``is $a_i$ joined to $b_j$?''}$$
Everything else is already determined.

## Case 3-in-$A$, 1-in-$B$: take $\{a_0, a_1, a_2, b_5\}$

- *Clique?* The pairs $a_0a_1, a_0a_2, a_1a_2$ are already joined ($A$ is a clique). We need
  the three cross pairs too. So: clique $\iff x[0][5] \wedge x[1][5] \wedge x[2][5]$.
- *Independent?* Impossible --- $a_0a_1$ is an edge.

So this set is homogeneous under exactly one 3-literal condition.
Count: 4 choices of triple from $A$, times 16 choices of $b$, $= 64$.

## Case 2-in-$A$, 2-in-$B$: take $\{a_0, a_1, b_3, b_7\}$

- *Clique?* Need $a_0a_1$ (yes), need **$b_3b_7$ to be an edge of the core** (fixed --- it
  either is or is not), plus all four cross edges. So *if* $b_3b_7$ is a core edge:
  $x[0][3] \wedge x[0][7] \wedge x[1][3] \wedge x[1][7]$, four literals. If it is not a core
  edge, this set can never be a clique.
- *Independent?* Impossible --- $a_0a_1$ again.

Count: $\binom{4}{2} = 6$ pairs, times 60 core edges, $= 360$.

## Case 1-in-$A$, 3-in-$B$: take $\{a_0, b_1, b_4, b_9\}$

Now both types are possible, depending on the core:

- *Clique*, if $b_1b_4b_9$ is a **triangle** in the core:
  $x[0][1] \wedge x[0][4] \wedge x[0][9]$.
- *Independent*, if $b_1b_4b_9$ is an **independent triple** in the core:
  $\neg x[0][1] \wedge \neg x[0][4] \wedge \neg x[0][9]$.

Count: $4 \times 56$ triangles $= 224$, plus $4 \times 56$ independent triples $= 224$.

## The two excluded cases

- **All four in $B$** --- impossible, the core is hom-4-free.
- **$A$ itself** --- it *is* a clique, but any set disjoint from $A$ lies entirely in $B$,
  and $B$ has no homogeneous 4-set. So $A$ can never be half of a disjoint pair.

**Total: $64 + 360 + 224 + 224 = 872$.**

## An actual clause

Take $P = \{a_0,a_1,a_2,b_5\}$ and $Q = \{a_3, b_1,b_4,b_9\}$ (with $b_1b_4b_9$ a core
triangle). These are **vertex-disjoint**. So we forbid both firing at once:
$$\neg x[0][5] \vee \neg x[1][5] \vee \neg x[2][5] \vee \neg x[3][1] \vee \neg x[3][4] \vee \neg x[3][9]$$

A 6-literal clause. Do that for every disjoint pair, giving $104{,}524$ clauses.

## A check you can do in your head

Clause length is the sum of the two conditions' literal counts. Which combinations are
possible?

| pairing | $A$-vertices used | length |
|---|---|---|
| (3A+1B) with (1A+3B) | $3+1 = 4$, fine | $3+3 = 6$ |
| (1A+3B) with (1A+3B) | $1+1 = 2$, fine | $3+3 = 6$ |
| (2A+2B) with (1A+3B) | $2+1 = 3$, fine | $4+3 = 7$ |
| (2A+2B) with (2A+2B) | $2+2 = 4$, fine | $4+4 = 8$ |
| (3A+1B) with (3A+1B) | $3+3 = 6 > 4$ | impossible |

So lengths can only be 6, 7, 8 --- and the reported histogram is exactly
$\{6: 43{,}840,\ 7: 52{,}416,\ 8: 8{,}268\}$. That is a consistency check derived from first
principles, and the sort of thing that would break loudly if the encoding were wrong.

A satisfying assignment would be a wiring of the 64 cross edges producing a graph with no
two disjoint homogeneous 4-sets. Both instances are UNSAT: no such wiring exists.

> **Insight.** The honest epistemics: you do not "understand" an UNSAT result the way you
> understand the pigeonhole argument. What you can check is (i) that the encoding faithfully
> says what it claims, and (ii) that the refutation certificate is valid. Both were done.
> That is the substitute for intuition here, and it is a normal situation in modern
> combinatorics --- the four-colour theorem has the same character.

\newpage

# Part 10: Why exactly two 16-vertex cores

**The engine.** Build hom-4-free graphs one vertex at a time.

**Why it is exhaustive** --- this is the crux:

> Every induced subgraph of a hom-4-free graph is hom-4-free.

(Obvious once stated: a homogeneous 4-set in the subgraph is one in the whole graph.)

So if $H$ is a hom-4-free graph on $n+1$ vertices, delete any vertex --- you get a
hom-4-free graph on $n$ vertices. Meaning **every** level-$(n{+}1)$ graph arises from
**some** level-$n$ graph by adding a vertex. If your level-$n$ list is complete, and you try
every admissible neighbourhood, your level-$(n{+}1)$ list is complete. Induct from the
trivial level 1.

**When is adding vertex $v$ with neighbourhood $S$ admissible?** A new homogeneous 4-set
must contain $v$, so it is $\{v\} \cup T$ for a triple $T$. Two ways to go wrong:

- $\{v\} \cup T$ is a $K_4$ $\iff$ $T \subseteq S$ and $T$ is a **triangle**. So: *no
  triangle inside $S$*.
- $\{v\} \cup T$ is independent $\iff$ $T \subseteq V \setminus S$ and $T$ is an
  **independent triple**. So: *no independent triple outside $S$*.

**And that bounds the search.** Since $G$ is hom-4-free, $\omega(G) \le 3$ and
$\alpha(G) \le 3$. Then $G[S]$ is triangle-free with $\alpha \le 3$, so by $R(3,4) = 9$ we
get $|S| \le 8$. Symmetrically $|V \setminus S| \le 8$. So
$$n - 8 \;\le\; |S| \;\le\; 8,$$
a huge pruning that makes the whole thing run in seconds.

**The output:**

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| count | 1 | 2 | 4 | 9 | 24 | 84 | 362 | 2079 | 14701 |

| $n$ | 10 | 11 | 12 | 13 | 14 | 15 | **16** | 17 | **18** |
|---|---|---|---|---|---|---|---|---|---|
| count | 103706 | 546356 | 1449166 | 1184231 | 130816 | 640 | **2** | 1 | **0** |

> **Insight.** The **0 at $n = 18$ is $R(4,4) = 18$ falling out as a by-product** --- "no
> hom-4-free graph on 18 vertices" is exactly Ramsey's statement. So the computation that
> establishes the catalogue also re-derives the theorem it depends on. If the code were
> buggy you would need a conspiracy: matching the published counts at every level, *and*
> landing on exactly 0 at 18, *and* exactly 2 at 16. That is the strongest internal evidence
> in the whole proof.

# Part 11: Paley(17), and a pleasing coincidence

Vertices are $\mathbb{Z}_{17}$; join $i$ and $j$ when $i - j$ is a nonzero **quadratic
residue** mod 17 --- the squares $\{1, 2, 4, 8, 9, 13, 15, 16\}$.

**It is a well-defined graph** because $-1 \equiv 16$ is itself a residue, so the relation
is symmetric.

**It is self-complementary.** Multiply every vertex by a *non*-residue: residues map to
non-residues, so edges map to non-edges. Hence Paley(17) is isomorphic to its own
complement --- which immediately gives $\omega = \alpha$.

**And that common value is 3.** $\omega \ge 3$ is easy: $\{0, 1, 2\}$ works, since
$1-0 = 1$, $2-1 = 1$, $2-0 = 2$ are all residues. That $\omega \le 3$ --- no $K_4$ --- is
the classical fact, and it is exactly *why* $R(4,4) > 17$. In our setting it also drops out
of the generation: Paley(17) is the unique survivor at level 17.

> **Insight.** Paley(17) is the standard lower-bound construction for $R(4,4) = 18$, *and*
> it is our lower-bound witness for $z(20) \ge 6$. Same graph, both jobs --- because both
> need the same property: *every homogeneous set is small*. Ramsey wants no homogeneous
> 4-set; we want groups of size at most 3, so that 17 vertices cannot fit in 5 groups.

\newpage

# Part 12: Self-test

If you can answer these unaided, you own the argument.

1. Why does the proof not need to consider the case where $A$ (the first homogeneous 4-set)
   is an independent set?

2. In the 2-in-$A$, 2-in-$B$ case, why does the *core* edge $b_3b_7$ matter, but the $A$
   edge $a_0a_1$ not?

3. Why can a (3A+1B) condition never pair with another (3A+1B) condition?

4. Where exactly does $R(4,4) = 18$ get used --- and where does the number 12 in
   "$z(12) \le 4$" come from?

5. Why does adding three isolated vertices to Paley(17) not reduce its cochromatic number?

6. What would it take to make the whole thing collapse --- that is, which single
   computational result, if wrong, breaks the proof?

# Part 13: The artifacts

Everything referenced here lives in `~/z20_repro/`:

| item | path |
|---|---|
| orderly generator (C + nauty) | `nauty/gen44.c` |
| cocolourability decision procedure | `nauty/cochk.c` |
| the two CNFs and DRUP certificates | `certificate/` |
| independent CNF regeneration + RUP checker | `verify_certificate.py` |
| `drat-trim` source, binary, regenerated CNFs, LRAT | `drat/` |
| `cake_lpr` (formally verified checker) | `cake_lpr/` |
| exact $c_6$ counter (subset DP) | `c6_fast.py` |
| result logs | `nauty/*_result.txt` |
| formal proof paper | `../z20_proof_paper.md` |
| Lean formalisation blueprint | `lean_blueprint.md` |

**Provenance.** Every mathematical step was produced by AI systems: a Nous Hermes agent
designed the original (unsuccessful) search harness driving GPT-5.6 Sol; GPT-5.6 Sol
contributed the structural reduction and the certificates; Claude carried out the
independent verification, the catalogue and Ramsey recomputation, the $z(8)$ and $z(12)$
re-derivations, the lower bound, and this document. The result should be treated as a
candidate proof pending independent scrutiny.
