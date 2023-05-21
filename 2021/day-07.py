#!/usr/bin/env python3

import os
import statistics

import pytest


def part1(inp: str) -> int:
	nums = tuple(int(line) for line in inp.split(","))
	return int(sum(abs(num - statistics.median(nums)) for num in nums))


def part2(inp: str) -> int:
	def getN(n: int) -> int:
		return sum(
			(abs(num - n) * (abs(num - n) + 1) // 2)
			for num in nums
		)
	nums = tuple(int(line) for line in inp.split(","))
	median = statistics.median(nums)
	num = getN(median)

	direction = {
		True: -1,
		False: 1,
	}[getN(median - 1) < num]

	while getN(median + direction) < num:
		median += direction
		num = getN(median)

	return int(num)


def main() -> int:
	inputPath = os.path.join(os.path.dirname(__file__), "input.txt")
	with open(inputPath) as inpF:
		inp = inpF.read().strip()
		print(f"Part 1: {part1(inp)}")
		print(f"Part 2: {part2(inp)}")
	return 0


EXAMPLE_INPUT = "16,1,2,0,4,2,7,1,2,14"


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 37),
	),
)
def testPart1(inp: str, expected: int):
	assert part1(inp) == expected


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 168),
	),
)
def testPart2(inp: str, expected: int):
	assert part2(inp) == expected


if __name__ == "__main__":
	raise SystemExit(main())
