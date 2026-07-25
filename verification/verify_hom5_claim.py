"""Verify the external review's central claim: do the 6 survivors contain
homogeneous 5-sets (=> provably 6-cocolourable via z(15)=5, hence never witnesses)?

Computes for each survivor: omega (clique no.), alpha (independence no.),
hom3/hom4/hom5 counts. Also re-verifies Paley(17) and the Goodman bound.
"""
from itertools import combinations

SURV = [
    (3,  "Stb^CmxaSsh{\\aK{iJPDZX`DWrrXBPIps", 43843),
    (24, "S~e[uNEo\\hIUHMI`cJiwz^S_RxjEUb[f?", 46018),
    (29, "StvSFAeqDBoyeqUohtXlQN|Ob\\pj]ax\\g", 61360),
    (37, "Stre}zwdcR?t[j]KKX`QcP\\KmRqyI_Azs", 52132),
    (50, "S~ecU]CqLtLY@{?VJQpj^[apwBHJbQ}B[", 56157),
    (57, "S{}sMJYiVCffP|IHgxi|bKE[YwhIeieQ{", 52281),
]

def decode(s):
    d = [ord(c) - 63 for c in s]; n = d[0]; bits = []
    for b in d[1:]:
        for k in range(5, -1, -1): bits.append((b >> k) & 1)
    adj = [set() for _ in range(n)]; idx = 0
    for j in range(1, n):
        for i in range(j):
            if idx < len(bits) and bits[idx]:
                adj[i].add(j); adj[j].add(i)
            idx += 1
    return n, adj

def hom_counts(n, adj, k):
    """count cliques and independent sets of size exactly k"""
    cl = ind = 0
    for q in combinations(range(n), k):
        qs = set(q)
        if all((qs - {v}) <= adj[v] for v in q): cl += 1
        elif all(not (adj[v] & qs) for v in q): ind += 1
    return cl, ind

def omega_alpha(n, adj):
    """max clique / max independent set size by growing k"""
    w = a = 1
    for k in range(2, n + 1):
        cl, ind = hom_counts(n, adj, k)
        if cl: w = k
        if ind: a = k
        if not cl and not ind: break
    return w, a

print("=== SURVIVORS: does each contain a homogeneous 5-set? ===")
print(f"{'iter':>4} {'m':>3} {'omega':>5} {'alpha':>5} {'hom3':>5} {'hom4':>5} {'hom5':>5}  {'HOM5?':>6}  c6")
any_hom5 = 0
for it, g6, c6 in SURV:
    n, adj = decode(g6)
    m = sum(len(a) for a in adj) // 2
    w, a = omega_alpha(n, adj)
    c3, i3 = hom_counts(n, adj, 3)
    c4, i4 = hom_counts(n, adj, 4)
    c5, i5 = hom_counts(n, adj, 5)
    h5 = c5 + i5
    any_hom5 += (1 if h5 else 0)
    print(f"{it:>4} {m:>3} {w:>5} {a:>5} {c3+i3:>5} {c4+i4:>5} {h5:>5}  {'YES' if h5 else 'no':>6}  {c6}")

print(f"\n  survivors WITH a homogeneous 5-set: {any_hom5}/6")

print("\n=== Goodman bound check (n=20): min homogeneous triples = n(n-2)(n-4)/24 ===")
print(f"  Goodman min = {20*18*16//24}")

print("\n=== Paley(17) re-verification ===")
QR = {(x*x) % 17 for x in range(1, 17)}
n = 17; adj = [set() for _ in range(n)]
for i in range(n):
    for j in range(i+1, n):
        if (i - j) % 17 in QR: adj[i].add(j); adj[j].add(i)
w, a = omega_alpha(n, adj)
c3, i3 = hom_counts(n, adj, 3); c4, i4 = hom_counts(n, adj, 4)
print(f"  n=17 m={sum(len(x) for x in adj)//2} omega={w} alpha={a} triangles={c3} indep-triples={i3} hom4={c4+i4}")

print("\n=== LEMMA CHECK (arithmetic of the pigeonhole argument) ===")
# six classes, sizes >=1 summing to 20: must have a class >=4; if all <=4, >=2 classes of size 4
bad = []
for parts in combinations(range(1, 21), 0):  # placeholder
    pass
def compositions(total, k, lo=1):
    if k == 1:
        if total >= lo: yield (total,)
        return
    for s in range(lo, total - (k-1)*lo + 1):
        for rest in compositions(total - s, k - 1, s):
            yield (s,) + rest
all_shapes = list(compositions(20, 6))
viol_ge4 = [s for s in all_shapes if max(s) < 4]
no5_shapes = [s for s in all_shapes if max(s) <= 4]
viol_two4 = [s for s in no5_shapes if sum(1 for x in s if x == 4) < 2]
print(f"  6-class shapes of 20: {len(all_shapes)}")
print(f"  shapes with NO class >=4: {len(viol_ge4)}  (claim: 0)")
print(f"  shapes with max<=4 but FEWER than two 4s: {len(viol_two4)}  (claim: 0)")
print(f"  shapes with max<=4 (the hom5-free admissible set): {[s for s in no5_shapes]}")
