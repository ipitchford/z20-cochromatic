#!/usr/bin/env python3
"""Semantic audit of the generated fixed-core CNFs."""
from __future__ import annotations
from itertools import combinations
from pathlib import Path
import random

from generate import CORE_G6, build_clauses, build_conditions, decode_graph6


def read_dimacs(path: Path):
    clauses = []
    with path.open(encoding="ascii") as source:
        header = next(line for line in source if line.startswith("p "))
        _, _, variables, declared = header.split()
        for line in source:
            if line.startswith("c") or not line.strip():
                continue
            values = tuple(map(int, line.split()))
            if values[-1] != 0:
                raise AssertionError("unterminated clause")
            clauses.append(values[:-1])
    if int(variables) != 64 or len(clauses) != int(declared):
        raise AssertionError("DIMACS header mismatch")
    return clauses


def direct_has_disjoint_homogeneous_quads(core_adj, assignment: int) -> bool:
    adjacency = [[False] * 20 for _ in range(20)]
    for i, j in combinations(range(4), 2):
        adjacency[i][j] = adjacency[j][i] = True
    for i, j in combinations(range(16), 2):
        adjacency[4 + i][4 + j] = adjacency[4 + j][4 + i] = core_adj[i][j]
    for a in range(4):
        for b in range(16):
            value = bool(assignment & (1 << (16 * a + b)))
            adjacency[a][4 + b] = adjacency[4 + b][a] = value

    homogeneous_masks = []
    for quad in combinations(range(20), 4):
        values = [adjacency[i][j] for i, j in combinations(quad, 2)]
        if all(values) or not any(values):
            homogeneous_masks.append(sum(1 << vertex for vertex in quad))
    return any(
        homogeneous_masks[i] & homogeneous_masks[j] == 0
        for i in range(len(homogeneous_masks))
        for j in range(i + 1, len(homogeneous_masks))
    )


def cnf_is_satisfied(clauses, assignment: int) -> bool:
    for clause in clauses:
        if not any(
            bool(assignment & (1 << (abs(literal) - 1))) == (literal > 0)
            for literal in clause
        ):
            return False
    return True


def main() -> None:
    here = Path(__file__).resolve().parent
    rng = random.Random(0x5A_20)
    for index, graph6 in enumerate(CORE_G6):
        core = decode_graph6(graph6)
        regenerated = build_clauses(build_conditions(core))
        stored = read_dimacs(here / f"z20_core{index}.cnf")
        if regenerated != stored:
            raise AssertionError(f"core {index}: stored CNF differs from regeneration")

        # The CNF is true exactly when no disjoint homogeneous-4 pair exists.
        # The instances are UNSAT, so random assignments should make both sides false.
        for _ in range(1000):
            assignment = rng.getrandbits(64)
            cnf_value = cnf_is_satisfied(stored, assignment)
            direct_value = not direct_has_disjoint_homogeneous_quads(core, assignment)
            if cnf_value != direct_value:
                raise AssertionError(f"core {index}: semantic mismatch")
        print(f"core {index}: exact regeneration and 1000 semantic spot-checks passed")


if __name__ == "__main__":
    main()
