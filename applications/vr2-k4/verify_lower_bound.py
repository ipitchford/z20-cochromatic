#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""Direct verifier for the 19-vertex lower bound for VR_2(K_4).

Red edges form the graph. Blue edges are non-edges. A monochromatic K4 is
therefore a homogeneous four-set. No third-party packages are required.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations

Q = {1, 2, 4, 8, 9, 13, 15, 16}


def require(condition: bool, message: str) -> None:
    """Exit with a machine-detectable failure if a verification check fails."""
    if not condition:
        raise SystemExit(f"verification failed: {message}")


def paley17() -> list[list[bool]]:
    adj = [[False] * 17 for _ in range(17)]
    for i, j in combinations(range(17), 2):
        adj[i][j] = adj[j][i] = ((i - j) % 17 in Q)
    return adj


def lower_witness() -> list[list[bool]]:
    """Replace vertex 9 of P17 by three independent twins 9,17,18."""
    base = paley17()
    outside = [v for v in range(17) if v != 9]
    twins = [9, 17, 18]
    adj = [[False] * 19 for _ in range(19)]

    for i, j in combinations(outside, 2):
        adj[i][j] = adj[j][i] = base[i][j]
    for t in twins:
        for v in outside:
            adj[t][v] = adj[v][t] = base[9][v]
    return adj


def homogeneous_four_sets(adj: list[list[bool]]) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for quad in combinations(range(len(adj)), 4):
        values = [adj[i][j] for i, j in combinations(quad, 2)]
        if all(values):
            out.append((sum(1 << v for v in quad), 1))
        elif not any(values):
            out.append((sum(1 << v for v in quad), 0))
    return out


def graph6(adj: list[list[bool]]) -> str:
    n = len(adj)
    if n >= 63:
        raise ValueError("small graph6 encoder supports n < 63")
    bits = [int(adj[i][j]) for j in range(1, n) for i in range(j)]
    bits.extend([0] * ((-len(bits)) % 6))
    chars = [chr(n + 63)]
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start:start + 6]:
            value = (value << 1) | bit
        chars.append(chr(value + 63))
    return "".join(chars)


def main() -> None:
    adj = lower_witness()
    h4 = homogeneous_four_sets(adj)
    masks = [mask for mask, _ in h4]
    colours = Counter(colour for _, colour in h4)
    disjoint_pair = any(
        masks[i] & masks[j] == 0
        for i in range(len(masks))
        for j in range(i + 1, len(masks))
    )
    edges = sum(adj[i][j] for i, j in combinations(range(19), 2))
    degrees = tuple(sorted(sum(row) for row in adj))

    require(edges == 84, f"expected 84 red edges, found {edges}")
    require(
        degrees == (8,) * 11 + (10,) * 8,
        f"unexpected degree sequence: {degrees}",
    )
    require(colours == Counter({0: 44}), f"unexpected K4 counts: {colours}")
    require(not disjoint_pair, "found a vertex-disjoint monochromatic pair")
    require(
        graph6(adj) == r"RzlXWmJpZDeJEJbDgp\EJsWnDlEJY?",
        f"unexpected graph6 encoding: {graph6(adj)}",
    )

    print("vertices: 19")
    print(f"red edges: {edges}")
    print(f"degree sequence: {degrees}")
    print(f"red K4s: {colours[1]}")
    print(f"blue K4s: {colours[0]}")
    print(f"disjoint monochromatic pair exists: {disjoint_pair}")
    print(f"graph6: {graph6(adj)}")
    print("All checks passed.")


if __name__ == "__main__":
    main()
