#!/usr/bin/env python3

import os

import pytest


def part1(inp: str) -> int:
	depths = tuple(int(line) for line in inp.splitlines())
	return sum(
		int(depths[i - 1] < depths[i])
		for i in range(1, len(depths))
	)


def part2(inp: str) -> int:
	depths = tuple(int(line) for line in inp.splitlines())
	return part1("\n".join(
		str(sum(depths[i:(i + 3)]))
		for i in range(len(depths) - 2)
	))


def main() -> int:
	inputPath = os.path.join("inputs", f"{__file__[-5:-3]:>02}.txt")
	with open(inputPath) as inpF:
		inp = inpF.read().strip()
		print(f"Part 1: {part1(inp)}")
		print(f"Part 2: {part2(inp)}")
	return 0


EXAMPLE_INPUT = """
199
200
208
210
200
207
240
269
260
263
""".strip()


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 7),
	),
)
def testPart1(inp: str, expected: int):
	assert part1(inp) == expected


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 5),
	),
)
def testPart2(inp: str, expected: int):
	assert part2(inp) == expected


if __name__ == "__main__":
	raise SystemExit(main())
