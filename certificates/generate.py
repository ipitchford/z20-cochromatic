#!/usr/bin/env python3
"""Generate the two fixed-core CNFs for the z(20) cochromatic search.

No third-party Python packages are required.  Variables are the 64 cross edges
x[a,b], with a in the fixed K4 A={0,1,2,3} and b in the 16-vertex
Ramsey(4,4)-core B={4,...,19}.  The CNF forbids every pair of vertex-disjoint
homogeneous 4-sets.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations
from pathlib import Path
import hashlib
import json

CORE_G6 = (
    "OsHHirKdlp[IFVI|KpqfR",
    "Ov?IXZIhlRWjUXL[iphst",
)


def decode_graph6(s: str) -> list[list[bool]]:
    """Decode graph6 for n<63 in McKay's standard order."""
    if not s:
        raise ValueError("empty graph6 string")
    n = ord(s[0]) - 63
    if not 0 <= n < 63:
        raise ValueError("this small decoder only supports n<63")
    bits: list[int] = []
    for c in s[1:]:
        value = ord(c) - 63
        if not 0 <= value < 64:
            raise ValueError(f"invalid graph6 character {c!r}")
        bits.extend((value >> k) & 1 for k in range(5, -1, -1))
    needed = n * (n - 1) // 2
    if len(bits) < needed:
        raise ValueError("truncated graph6 payload")
    adj = [[False] * n for _ in range(n)]
    p = 0
    for j in range(1, n):
        for i in range(j):
            adj[i][j] = adj[j][i] = bool(bits[p])
            p += 1
    return adj


def edge_count(adj: list[list[bool]]) -> int:
    return sum(adj[i][j] for j in range(len(adj)) for i in range(j))


def degree_sequence(adj: list[list[bool]]) -> list[int]:
    return sorted(sum(row) for row in adj)


def homogeneous(adj: list[list[bool]], vertices: tuple[int, ...]) -> bool:
    values = [adj[i][j] for i, j in combinations(vertices, 2)]
    return all(values) or not any(values)


def triangle_counts(adj: list[list[bool]]) -> tuple[int, int]:
    triangles = independent_triples = 0
    for triple in combinations(range(len(adj)), 3):
        values = [adj[i][j] for i, j in combinations(triple, 2)]
        triangles += all(values)
        independent_triples += not any(values)
    return triangles, independent_triples


def cross_var(a: int, b: int) -> int:
    """DIMACS variable for cross edge from anchor a to core vertex b."""
    return 1 + 16 * a + b


def build_conditions(adj: list[list[bool]]):
    """Return every possible mixed homogeneous 4-set and its cross literals.

    Each condition is (20-vertex bitmask, tuple of literals whose conjunction
    makes that 4-set homogeneous, descriptive tag).
    """
    conditions = []

    # 3 vertices in A and 1 in B: only a clique can occur.
    for anchor_vertices in combinations(range(4), 3):
        for b in range(16):
            vertex_mask = sum(1 << a for a in anchor_vertices) | (1 << (4 + b))
            literals = tuple(cross_var(a, b) for a in anchor_vertices)
            conditions.append((vertex_mask, literals, "3A+1B clique"))

    # 2 in A and 2 in B: only a clique, and the B-pair must be an edge.
    for anchor_vertices in combinations(range(4), 2):
        for b, c in combinations(range(16), 2):
            if adj[b][c]:
                vertex_mask = (
                    sum(1 << a for a in anchor_vertices)
                    | (1 << (4 + b))
                    | (1 << (4 + c))
                )
                literals = tuple(
                    cross_var(a, core_vertex)
                    for a in anchor_vertices
                    for core_vertex in (b, c)
                )
                conditions.append((vertex_mask, literals, "2A+2B clique"))

    # 1 in A and 3 in B: clique or independent set according to the B-triple.
    for a in range(4):
        for core_vertices in combinations(range(16), 3):
            values = [adj[i][j] for i, j in combinations(core_vertices, 2)]
            if all(values):
                literals = tuple(cross_var(a, b) for b in core_vertices)
                kind = "1A+3B clique"
            elif not any(values):
                literals = tuple(-cross_var(a, b) for b in core_vertices)
                kind = "1A+3B independent"
            else:
                continue
            vertex_mask = (1 << a) | sum(1 << (4 + b) for b in core_vertices)
            conditions.append((vertex_mask, literals, kind))

    return conditions


def build_clauses(conditions):
    clauses: list[tuple[int, ...]] = []
    for i, (mask_i, literals_i, _) in enumerate(conditions):
        for mask_j, literals_j, _ in conditions[i + 1 :]:
            if mask_i & mask_j:
                continue
            # Negate the two homogeneity conjunctions.
            clause = tuple(-literal for literal in literals_i + literals_j)
            if len({abs(literal) for literal in clause}) != len(clause):
                raise AssertionError("disjoint 4-sets unexpectedly share a cross variable")
            clauses.append(clause)
    return clauses


def write_dimacs(path: Path, clauses: list[tuple[int, ...]]) -> None:
    with path.open("w", encoding="ascii", newline="\n") as output:
        output.write(f"p cnf 64 {len(clauses)}\n")
        for clause in clauses:
            output.write(" ".join(map(str, clause)) + " 0\n")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def generate(output_dir: Path) -> list[dict[str, object]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    metadata = []
    for index, graph6 in enumerate(CORE_G6):
        adj = decode_graph6(graph6)
        if len(adj) != 16:
            raise AssertionError("core order is not 16")
        if edge_count(adj) != 60:
            raise AssertionError("core edge count is not 60")
        if any(homogeneous(adj, quad) for quad in combinations(range(16), 4)):
            raise AssertionError("core is not a Ramsey(4,4,16)-graph")

        conditions = build_conditions(adj)
        clauses = build_clauses(conditions)
        condition_types = Counter(tag for _, _, tag in conditions)
        clause_lengths = Counter(map(len, clauses))

        expected_condition_types = Counter(
            {
                "3A+1B clique": 64,
                "2A+2B clique": 360,
                "1A+3B clique": 224,
                "1A+3B independent": 224,
            }
        )
        if condition_types != expected_condition_types:
            raise AssertionError((condition_types, expected_condition_types))
        if len(conditions) != 872 or len({mask for mask, _, _ in conditions}) != 872:
            raise AssertionError("unexpected mixed homogeneous-4-set count")
        if clause_lengths != Counter({6: 43840, 7: 52416, 8: 8268}):
            raise AssertionError(clause_lengths)
        if len(clauses) != 104_524:
            raise AssertionError("unexpected clause count")

        cnf_path = output_dir / f"z20_core{index}.cnf"
        write_dimacs(cnf_path, clauses)
        triangles, independent_triples = triangle_counts(adj)
        metadata.append(
            {
                "core": index,
                "graph6": graph6,
                "vertices": 16,
                "edges": edge_count(adj),
                "degree_sequence": degree_sequence(adj),
                "triangles": triangles,
                "independent_triples": independent_triples,
                "homogeneous_4_sets": 0,
                "mixed_homogeneous_4_conditions": len(conditions),
                "clauses": len(clauses),
                "clause_lengths": dict(sorted(clause_lengths.items())),
                "cnf_sha256": sha256(cnf_path),
            }
        )

    with (output_dir / "metadata.json").open("w", encoding="utf-8") as output:
        json.dump(metadata, output, indent=2)
        output.write("\n")
    return metadata


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    records = generate(here)
    for record in records:
        print(json.dumps(record, sort_keys=True))
