#!/usr/bin/env python3

import os
from collections import defaultdict
from collections import deque

import pytest


def part1(inp: str) -> int:
	edges: dict[str, set] = defaultdict(set)
	for line in inp.splitlines():
		src, dest = line.split("-")
		edges[src].add(dest)
		edges[dest].add(src)

	done = set()
	todo: deque[tuple[str, ...]] = deque([("start",)])
	while todo:
		path = todo.popleft()
		if path[-1] == "end":
			done.add(path)
			continue
		for p in edges[path[-1]]:
			if p.isupper() or p not in path:
				todo.append((*path, p))

	return len(done)


def part2(inp: str) -> int:
	edges: dict[str, set] = defaultdict(set)
	for line in inp.splitlines():
		src, dest = line.split("-")
		edges[src].add(dest)
		edges[dest].add(src)

	done = set()
	todo: deque[tuple[tuple[str, ...], bool]] = deque([(("start",), False)])
	while todo:
		path, double = todo.popleft()
		if path[-1] == "end":
			done.add(path)
			continue

		for p in edges[path[-1]] - {"start"}:
			if p.isupper():
				todo.append(((*path, p), double))
			elif double is False and path.count(p) == 1:
				todo.append(((*path, p), True))
			elif p not in path:
				todo.append(((*path, p), double))

	return len(done)


def main() -> int:
	inputPath = os.path.join(os.path.dirname(__file__), "input.txt")
	with open(inputPath) as inpF:
		inp = inpF.read().strip()
		print(f"Part 1: {part1(inp)}")
		print(f"Part 2: {part2(inp)}")
	return 0


EXAMPLE_INPUT_1 = """
start-A
start-b
A-c
A-b
b-d
A-end
b-end
""".strip()

EXAMPLE_INPUT_2 = """
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
""".strip()

EXAMPLE_INPUT_3 = """
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
""".strip()


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT_1, 10),
		pytest.param(EXAMPLE_INPUT_2, 19),
		pytest.param(EXAMPLE_INPUT_3, 226),
	),
)
def testPart1(inp: str, expected: int):
	assert part1(inp) == expected


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT_1, 36),
		pytest.param(EXAMPLE_INPUT_2, 103),
		pytest.param(EXAMPLE_INPUT_3, 3509),
	),
)
def testPart2(inp: str, expected: int):
	assert part2(inp) == expected


if __name__ == "__main__":
	raise SystemExit(main())
