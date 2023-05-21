#!/usr/bin/env python3

import os
from collections import defaultdict
from math import prod
from typing import Generator

import pytest


def neighbours(x: int, y: int) -> Generator[tuple[int, int], None, None]:
	yield (x + 1, y)
	yield (x - 1, y)
	yield (x, y + 1)
	yield (x, y - 1)


def part1(inp: str) -> int:
	coords = defaultdict(int, {
		(x, y): int(char)
		for y, line in enumerate(inp.splitlines())
		for x, char in enumerate(line)
	})

	return sum((i + 1) * int(all(coords.get(at, 9) > i for at in neighbours(x, y))) for (x, y), i in coords.items())


def part2(inp: str) -> int:
	coords = defaultdict(int, {
		(x, y): int(char)
		for y, line in enumerate(inp.splitlines())
		for x, char in enumerate(line)
	})

	top3 = [0, 0, 0]

	for (x, y), i in coords.items():
		if all(coords.get(at, 9) > i for at in neighbours(x, y)):
			seen = set()
			todo = [(x, y)]
			while todo:
				x, y = todo.pop()
				seen.add((x, y))

				for other in neighbours(x, y):
					if other not in seen and coords.get(other, 9) != 9:
						todo.append(other)

			if len(seen) > min(top3):
				top3.remove(min(top3))
				top3.append(len(seen))

	return prod(top3)


def main() -> int:
	inputPath = os.path.join(os.path.dirname(__file__), "input.txt")
	with open(inputPath) as inpF:
		inp = inpF.read().strip()
		print(f"Part 1: {part1(inp)}")
		print(f"Part 2: {part2(inp)}")
	return 0


EXAMPLE_INPUT = """
2199943210
3987894921
9856789892
8767896789
9899965678
""".strip()


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 15),
	),
)
def testPart1(inp: str, expected: int):
	assert part1(inp) == expected


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 1134),
	),
)
def testPart2(inp: str, expected: int):
	assert part2(inp) == expected


if __name__ == "__main__":
	raise SystemExit(main())
