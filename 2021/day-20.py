#!/usr/bin/env python3

import functools
import os
from collections import defaultdict

import pytest


def getIdx(coords: dict[tuple[int, int], bool], x: int, y: int) -> int:
	_coords = (
		coords[x - 1, y - 1], coords[x, y - 1], coords[x + 1, y - 1],
		coords[x - 1, y], coords[x, y], coords[x + 1, y],
		coords[x - 1, y + 1], coords[x, y + 1], coords[x + 1, y + 1],
	)
	return int("".join(str(int(n)) for n in _coords), 2)


def compute(inp: str, iterations: int) -> int:
	idxString, imageLines = inp.split("\n\n")

	index = defaultdict(bool)
	for i, c in enumerate(idxString.strip()):
		index[i] = (c == "#")

	image = defaultdict(bool)
	for y, line in enumerate(imageLines.splitlines()):
		for x, c in enumerate(line):
			image[(x, y)] = (c == "#")

	for i in range(iterations):
		numsX = tuple(int(x) for x, _ in image)
		numsY = tuple(int(y) for _, y in image)

		minX, maxX = min(numsX), max(numsX)
		minY, maxY = min(numsY), max(numsY)

		if index[0] and not index[511]:
			newImage = defaultdict(functools.partial(lambda j: j % 2 == 0, j=i))
		else:
			newImage = defaultdict(bool)

		for y in range(minY - 1, maxY + 2):
			for x in range(minX - 1, maxX + 2):
				newImage[(x, y)] = bool(index[getIdx(image, x, y)])

		image = newImage

	return sum(image.values())


def main() -> int:
	inputPath = os.path.join(os.path.dirname(__file__), "input.txt")
	with open(inputPath) as inpF:
		inp = inpF.read().strip()
		print(f"Part 1: {compute(inp, 2)}")
		print(f"Part 2: {compute(inp, 50)}")
	return 0


EXAMPLE_INPUT = """
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
""".strip()


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 35),
	),
)
def testPart1(inp: str, expected: int):
	assert compute(inp, 2) == expected


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 3351),
	),
)
def testPart2(inp: str, expected: int):
	assert compute(inp, 50) == expected


if __name__ == "__main__":
	raise SystemExit(main())
