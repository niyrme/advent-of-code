#!/usr/bin/env python3

import os
from typing import NamedTuple

import pytest


class Direction(NamedTuple):
	x: int
	y: int


RIGHT = Direction(1, 0)
DOWN = Direction(0, 1)


def part1(inp: str) -> int:
	lines = inp.splitlines()
	coords: dict[tuple[int, int], Direction] = dict()
	for y, line in enumerate(lines):
		for x, char in enumerate(line):
			if char == ".":
				continue
			coords[(x, y)] = {"v": DOWN, ">": RIGHT}[char]

	i = 0
	while True:
		i += 1

		newCoords1: dict[tuple[int, int], Direction] = dict()
		for (x, y), direction in coords.items():
			pos = (x, y)
			if direction == RIGHT:
				newPos = (
					(x + direction.x) % len(lines[0]),
					(y + direction.y) % len(lines),
				)
				if newPos not in coords:
					pos = newPos
			newCoords1[pos] = direction

		newCoords2: dict[tuple[int, int], Direction] = dict()
		for (x, y), direction in newCoords1.items():
			pos = (x, y)
			if direction == DOWN:
				newPos = (
					(x + direction.x) % len(lines[0]),
					(y + direction.y) % len(lines),
				)
				if newPos not in newCoords1:
					pos = newPos
			newCoords2[pos] = direction

		if newCoords2 == coords:
			break
		else:
			coords = newCoords2

	return i


def main() -> int:
	inputPath = os.path.join(os.path.dirname(__file__), "input.txt")
	with open(inputPath) as inpF:
		inp = inpF.read().strip()
		print(f"Part 1: {part1(inp)}")
	return 0


EXAMPLE_INPUT = """
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
""".strip()


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 58),
	),
)
def testPart1(inp: str, expected: int):
	assert part1(inp) == expected


if __name__ == "__main__":
	raise SystemExit(main())
