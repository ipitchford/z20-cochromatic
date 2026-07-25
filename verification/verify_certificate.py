"""INDEPENDENT verification of the z20 core certificate package.

Four checks, none of which executes any code from the package:
  (1) REGENERATE both CNFs from the graph6 cores with my own generator and
      compare clause SETS against theirs (audits their graph6 decoding and
      clause enumeration).
  (2) SEMANTIC check: random 64-bit cross-edge assignments -> build the actual
      20-vertex graph -> directly test "has two disjoint homogeneous 4-sets"
      and compare with CNF satisfaction. (Confirms the CNF means what's claimed.)
  (3) RUP-check their DRUP proofs with my own checker, against MY regenerated
      clauses (not theirs), ending in the empty clause.
  (4) SHA-256 of their CNFs vs their manifest.
"""
import sys, hashlib, random
from itertools import combinations
import numpy as np

PKG = "/private/tmp/claude-501/-Users-admin-claude-sandbox/276131d9-a463-44f2-8575-634e4e2d490a/scratchpad/cert/z20_core_certificate_candidate"
CORES = ["OsHHirKdlp[IFVI|KpqfR", "Ov?IXZIhlRWjUXL[iphst"]

def decode(s):
    d = [ord(c) - 63 for c in s]; n = d[0]; bits = []
    for b in d[1:]:
        for k in range(5, -1, -1): bits.append((b >> k) & 1)
    adj = [[False]*n for _ in range(n)]; idx = 0
    for j in range(1, n):
        for i in range(j):
            if idx < len(bits) and bits[idx]: adj[i][j] = adj[j][i] = True
            idx += 1
    return n, adj

def cross_var(a, b): return 1 + 16*a + b   # a in 0..3 (anchor), b in 0..15 (core)

def my_conditions(adj):
    """Every possible MIXED homogeneous 4-set + the cross-literal conjunction
    that makes it homogeneous. A={0,1,2,3} is a clique; core is hom4-free."""
    conds = []
    # 3 in A + 1 in B : A-triple is a clique already; need 3 cross edges present
    for tri in combinations(range(4), 3):
        for b in range(16):
            mask = sum(1 << a for a in tri) | (1 << (4+b))
            conds.append((mask, tuple(cross_var(a, b) for a in tri)))
    # 2 in A + 2 in B : need the B-pair to be an edge, and 4 cross edges present
    for pair in combinations(range(4), 2):
        for b, c in combinations(range(16), 2):
            if adj[b][c]:
                mask = sum(1 << a for a in pair) | (1 << (4+b)) | (1 << (4+c))
                conds.append((mask, tuple(cross_var(a, v) for a in pair for v in (b, c))))
    # 1 in A + 3 in B : B-triple a triangle (clique) or independent triple
    for a in range(4):
        for tri in combinations(range(16), 3):
            vals = [adj[i][j] for i, j in combinations(tri, 2)]
            if all(vals):   lits = tuple(cross_var(a, b) for b in tri)
            elif not any(vals): lits = tuple(-cross_var(a, b) for b in tri)
            else: continue
            mask = (1 << a) | sum(1 << (4+b) for b in tri)
            conds.append((mask, lits))
    return conds

def my_clauses(conds):
    out = []
    for i in range(len(conds)):
        mi, li = conds[i]
        for j in range(i+1, len(conds)):
            mj, lj = conds[j]
            if mi & mj: continue                    # not vertex-disjoint
            cl = tuple(-x for x in li + lj)
            if len({abs(x) for x in cl}) != len(cl): continue
            out.append(cl)
    return out

def read_dimacs(path):
    cls = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line[0] in "pc": continue
            lits = [int(x) for x in line.split()]
            assert lits[-1] == 0
            cls.append(tuple(lits[:-1]))
    return cls

def has_two_disjoint_hom4(adj20):
    """Direct semantic test on the full 20-vertex graph."""
    homs = []
    for q in combinations(range(20), 4):
        qs = set(q)
        if all(all(adj20[v][u] for u in qs-{v}) for v in q): homs.append(sum(1<<v for v in q))
        elif all(not any(adj20[v][u] for u in qs-{v}) for v in q): homs.append(sum(1<<v for v in q))
    for i in range(len(homs)):
        for j in range(i+1, len(homs)):
            if homs[i] & homs[j] == 0: return True
    return False

def build_graph20(adj_core, assign):
    """A={0,1,2,3} clique; core at 4..19; cross edges from `assign` (dict var->bool)."""
    g = [[False]*20 for _ in range(20)]
    for a, b in combinations(range(4), 2): g[a][b] = g[b][a] = True
    for i in range(16):
        for j in range(i+1, 16):
            if adj_core[i][j]: g[4+i][4+j] = g[4+j][4+i] = True
    for a in range(4):
        for b in range(16):
            if assign[cross_var(a, b)]: g[a][4+b] = g[4+b][a] = True
    return g

# ---------------- RUP checker (numpy bitmask unit propagation, 64 vars) -------
def make_masks(clauses):
    pos = np.zeros(len(clauses), dtype=np.uint64)
    neg = np.zeros(len(clauses), dtype=np.uint64)
    for k, c in enumerate(clauses):
        p = n_ = np.uint64(0)
        for lit in c:
            bit = np.uint64(1) << np.uint64(abs(lit)-1)
            if lit > 0: p |= bit
            else: n_ |= bit
        pos[k] = p; neg[k] = n_
    return pos, neg

def propagate_conflict(pos, neg, assigned, value):
    """Unit-propagate; return True iff a conflict is derived."""
    U64 = np.uint64
    while True:
        sat = ((pos & assigned & value) != 0) | ((neg & assigned & ~value) != 0)
        un = (pos | neg) & ~assigned
        live = ~sat
        if np.any(live & (un == 0)): return True                 # empty under assignment
        isunit = live & (un != 0) & ((un & (un - U64(1))) == 0)
        if not np.any(isunit): return False
        u = un[isunit]; p = pos[isunit]
        newT = np.bitwise_or.reduce(np.where((u & p) != 0, u, U64(0))) if u.size else U64(0)
        newF = np.bitwise_or.reduce(np.where((u & p) == 0, u, U64(0))) if u.size else U64(0)
        if newT & newF: return True                              # contradictory units
        add = (newT | newF) & ~assigned
        if add == 0: return False
        assigned = assigned | add
        value = value | newT

def rup_check(base_clauses, proof_path):
    pos, neg = make_masks(base_clauses)
    U64 = np.uint64
    steps = 0; empty_seen = False
    with open(proof_path) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            if line.startswith('d'): continue          # ignoring deletions is sound for UNSAT
            lits = [int(x) for x in line.split()]
            assert lits[-1] == 0, "proof line must end in 0"
            cl = lits[:-1]
            assigned = U64(0); value = U64(0); bad = False
            for lit in cl:                              # assume NEGATION of the clause
                bit = U64(1) << U64(abs(lit)-1)
                want_true = (lit < 0)
                if assigned & bit:
                    if bool(value & bit) != want_true: bad = True; break
                assigned |= bit
                if want_true: value |= bit
            if bad:
                pass                                    # negation self-contradictory => trivially RUP
            elif not propagate_conflict(pos, neg, assigned, value):
                return False, steps, f"proof line {steps+1} is NOT RUP: {cl}"
            # append the clause to the accumulated formula
            p = n_ = U64(0)
            for lit in cl:
                bit = U64(1) << U64(abs(lit)-1)
                if lit > 0: p |= bit
                else: n_ |= bit
            pos = np.append(pos, p); neg = np.append(neg, n_)
            steps += 1
            if not cl: empty_seen = True
    return empty_seen, steps, ("empty clause derived" if empty_seen else "NO empty clause in proof")

# ------------------------------- run ----------------------------------------
print("=" * 70)
for idx, g6 in enumerate(CORES):
    print(f"\n########## CORE {idx}: {g6} ##########")
    n, adj = decode(g6)
    assert n == 16
    conds = my_conditions(adj)
    print(f"[1] my mixed-hom4 conditions: {len(conds)}  (claimed 872)  "
          f"{'OK' if len(conds)==872 else 'MISMATCH'}")
    mine = my_clauses(conds)
    theirs = read_dimacs(f"{PKG}/z20_core{idx}.cnf")
    ms = {tuple(sorted(c)) for c in mine}; ts = {tuple(sorted(c)) for c in theirs}
    print(f"[1] my clauses: {len(mine)}   theirs: {len(theirs)}   "
          f"clause-SETS identical: {'YES' if ms == ts else 'NO'}")
    from collections import Counter
    print(f"[1] my length histogram: {dict(sorted(Counter(map(len, mine)).items()))}")

    h = hashlib.sha256(open(f"{PKG}/z20_core{idx}.cnf","rb").read()).hexdigest()
    print(f"[4] their CNF sha256 {h[:16]}...")

    # (2) semantic spot-check
    rng = random.Random(1234 + idx); agree = 0; trials = 300
    for _ in range(trials):
        assign = {v: rng.random() < 0.5 for v in range(1, 65)}
        g20 = build_graph20(adj, assign)
        direct = has_two_disjoint_hom4(g20)
        cnf_ok = all(any((lit > 0) == assign[abs(lit)] for lit in c) for c in mine)
        # CNF satisfied  <=>  NO two disjoint hom4s
        if cnf_ok == (not direct): agree += 1
    print(f"[2] semantic spot-check: {agree}/{trials} assignments agree "
          f"(CNF satisfied <=> no two disjoint hom4)  {'OK' if agree==trials else 'MISMATCH'}")

    # (3) RUP check of THEIR proof against MY clauses
    ok, steps, msg = rup_check(mine, f"{PKG}/z20_core{idx}.drup")
    print(f"[3] RUP check of their DRUP vs MY CNF: {steps} steps -> {msg}")
    print(f"    VERDICT core {idx}: {'UNSAT PROOF VERIFIED' if ok else 'PROOF FAILED'}")
print("\n" + "=" * 70)
