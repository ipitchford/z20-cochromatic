"""Fast exact c6 counter: memoized subset DP, canonicalised on the least-indexed
vertex of each block (so each unordered partition is counted exactly once).

c6(G) = number of partitions of V into exactly 6 non-empty homogeneous blocks
(each block a clique or an independent set).

count(mask, k) = ways to partition `mask` into exactly k homogeneous blocks
               = sum over homogeneous B subset-of mask with min(mask) in B
                 of count(mask \\ B, k-1)
"""
from functools import lru_cache

def decode(s):
    d = [ord(c) - 63 for c in s]; n = d[0]; bits = []
    for b in d[1:]:
        for k in range(5, -1, -1): bits.append((b >> k) & 1)
    adjm = [0] * n; idx = 0
    for j in range(1, n):
        for i in range(j):
            if idx < len(bits) and bits[idx]:
                adjm[i] |= 1 << j; adjm[j] |= 1 << i
            idx += 1
    return n, adjm

def homogeneous_sets(n, adj):
    """All homogeneous subsets of size>=1, grouped by their minimum vertex."""
    by_min = [[] for _ in range(n)]
    # grow cliques and independent sets separately from each min vertex
    def grow(v, cur_mask, cand, is_clique):
        by_min[v].append(cur_mask)
        c = cand
        while c:
            u_bit = c & -c; c ^= u_bit
            u = u_bit.bit_length() - 1
            nxt = (cand & adj[u]) if is_clique else (cand & ~adj[u])
            nxt &= ~((1 << (u + 1)) - 1)          # only higher-indexed
            grow(v, cur_mask | u_bit, nxt, is_clique)
    for v in range(n):
        higher = ~((1 << (v + 1)) - 1) & ((1 << n) - 1)
        grow(v, 1 << v, higher & adj[v], True)          # cliques
        grow(v, 1 << v, higher & ~adj[v] & ((1<<n)-1), False)  # independent
    # dedupe (singletons counted twice: clique and independent)
    return [sorted(set(lst)) for lst in by_min]

def c6(n, adj, k_target=6):
    by_min = homogeneous_sets(n, adj)
    maxblk = max((bin(m).count('1') for lst in by_min for m in lst), default=1)
    from sys import setrecursionlimit; setrecursionlimit(10000)
    memo = {}
    def count(mask, k):
        if mask == 0: return 1 if k == 0 else 0
        if k == 0: return 0
        sz = bin(mask).count('1')
        if sz < k or sz > k * maxblk: return 0     # feasibility pruning
        key = (mask, k)
        r = memo.get(key)
        if r is not None: return r
        v = (mask & -mask).bit_length() - 1
        tot = 0
        for B in by_min[v]:
            if B & ~mask: continue
            tot += count(mask ^ B, k - 1)
        memo[key] = tot
        return tot
    return count((1 << n) - 1, k_target)

def c6_from_graph6(s):
    n, adj = decode(s)
    return c6(n, adj)

if __name__ == "__main__":
    import time
    KNOWN = [
        ("Stb^CmxaSsh{\\aK{iJPDZX`DWrrXBPIps", 43843),
        ("S~e[uNEo\\hIUHMI`cJiwz^S_RxjEUb[f?", 46018),
        ("StvSFAeqDBoyeqUohtXlQN|Ob\\pj]ax\\g", 61360),
        ("Stre}zwdcR?t[j]KKX`QcP\\KmRqyI_Azs", 52132),
        ("S~ecU]CqLtLY@{?VJQpj^[apwBHJbQ}B[", 56157),
        ("S{}sMJYiVCffP|IHgxi|bKE[YwhIeieQ{", 52281),
    ]
    print("=== validating fast counter against known exact c6 values ===")
    ok = True
    for g6, exp in KNOWN:
        t0 = time.time(); got = c6_from_graph6(g6); dt = time.time() - t0
        good = (got == exp); ok &= good
        print(f"  {'OK ' if good else 'MISMATCH'} got={got:>7} expected={exp:>7}  {dt:.2f}s")
    # timing on a random graph (high c6 -> worst case)
    import random
    rng = random.Random(101); N = 20
    adjm = [0]*N
    for i in range(N):
        for j in range(i+1, N):
            if rng.random() < 0.5: adjm[i] |= 1<<j; adjm[j] |= 1<<i
    t0 = time.time(); val = c6(N, adjm); dt = time.time() - t0
    print(f"  random seed101: c6={val:,} in {dt:.2f}s  (earlier enumerator gave 1,785,917)")
    print("ALL MATCH" if ok else "FAILED")
