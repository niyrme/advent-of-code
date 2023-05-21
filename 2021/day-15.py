#!/usr/bin/env python3

import os
from queue import PriorityQueue
from typing import Generator

import pytest


def mod(n: int) -> int:
	while n > 9:
		n -= 9
	return n


def nextPos(x: int, y: int) -> Generator[tuple[int, int], None, None]:
	# prioritize right and bottom
	yield (x, y + 1)
	yield (x + 1, y)
	yield (x, y - 1)
	yield (x - 1, y)


def getPath(coords: dict[tuple[int, int], int]) -> int:
	lastXY = max(coords)

	bestAt = dict()

	todo = PriorityQueue()
	todo.put((0, (0, 0)))

	while not todo.empty():
		cost, lastPos = todo.get()

		if lastPos in bestAt and cost >= bestAt[lastPos]:
			continue
		else:
			bestAt[lastPos] = cost

		if lastPos == lastXY:
			return cost

		for np in nextPos(*lastPos):
			if np in coords:
				todo.put((cost + coords[np], np))

	raise AssertionError("unreachable")


def part1(inp: str) -> int:
	return getPath({
		(x, y): int(v)
		for y, line in enumerate(inp.splitlines())
		for x, v in enumerate(line)
	})


def part2(inp: str) -> int:
	return getPath({
		# assume square
		(iX * len(line) + x, iY * len(line) + y): mod(int(v) + iX + iY)
		for y, line in enumerate(inp.splitlines())
		for x, v in enumerate(line)
		for iY in range(5)
		for iX in range(5)
	})


def main() -> int:
	inputPath = os.path.join(os.path.dirname(__file__), "input.txt")
	with open(inputPath) as inpF:
		inp = inpF.read().strip()
		print(f"Part 1: {part1(inp)}")
		print(f"Part 2: {part2(inp)}")
	return 0


EXAMPLE_INPUT = """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
""".strip()


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 40),
	),
)
def testPart1(inp: str, expected: int):
	assert part1(inp) == expected


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 315),
	),
)
def testPart2(inp: str, expected: int):
	assert part2(inp) == expected


if __name__ == "__main__":
	raise SystemExit(main())
