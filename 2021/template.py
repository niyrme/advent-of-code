#!/usr/bin/env python3

import os

import pytest


def part1(inp: str) -> int:
	lines = inp.splitlines()
	for line in lines:
		...

	raise NotImplementedError


def part2(inp: str) -> int:
	lines = inp.splitlines()
	for line in lines:
		...

	raise NotImplementedError


def main() -> int:
	inputPath = os.path.join("inputs", f"{__file__[-5:-3]:>02}.txt")
	with open(inputPath) as inpF:
		inp = inpF.read().strip()
		print(f"Part 1: {part1(inp)}")
		print(f"Part 2: {part2(inp)}")
	return 0


EXAMPLE_INPUT = """

""".strip()


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 0),
	),
)
def testPart1(inp: str, expected: int):
	assert part1(inp) == expected


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 0),
	),
)
def testPart2(inp: str, expected: int):
	assert part2(inp) == expected


if __name__ == "__main__":
	raise SystemExit(main())
