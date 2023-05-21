#!/usr/bin/env python3

import os
from collections import Counter
from typing import Sequence

import pytest


def getFishCount(inp: Sequence[int], days: int) -> int:
	fish = Counter(inp)

	for _ in range(days):
		_fish = Counter({8: fish[0], 6: fish[0]})
		_fish.update({k - 1: v for k, v in fish.items() if k > 0})
		fish = _fish

	return sum(fish.values())


def part1(inp: str) -> int:
	return getFishCount(tuple(int(line) for line in inp.split(",")), 80)


def part2(inp: str) -> int:
	return getFishCount(tuple(int(line) for line in inp.split(",")), 256)


def main() -> int:
	inputPath = os.path.join(os.path.dirname(__file__), "input.txt")
	with open(inputPath) as inpF:
		inp = inpF.read().strip()
		print(f"Part 1: {part1(inp)}")
		print(f"Part 2: {part2(inp)}")
	return 0


EXAMPLE_INPUT = "3,4,3,1,2"


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 5934),
	),
)
def testPart1(inp: str, expected: int):
	assert part1(inp) == expected


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 26984457539),
	),
)
def testPart2(inp: str, expected: int):
	assert part2(inp) == expected


if __name__ == "__main__":
	raise SystemExit(main())
