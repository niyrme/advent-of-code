#!/usr/bin/env python3

import os
from typing import Literal
from typing import Sequence
from typing import Union

import pytest


def cmp(a: int, b: int) -> int:
	return int(a > b) - int(a < b)


def part1(inp: str) -> int:
	bitString = "".join(
		{True: "0", False: "1"}[str(x).count("0") > str(x).count("1")]
		for x in (
			"".join(i)
			for i in zip(*tuple(line for line in inp.splitlines()))
		)
	)

	return int(bitString, 2) * int("".join("1" if x == "0" else "0" for x in bitString), 2)


def mostCommon(bitStrings: Sequence[str], pos: int) -> Union[Literal[0, 1], None]:
	bitRow = "".join(list(zip(*bitStrings))[pos])

	count0 = bitRow.count("0")
	count1 = bitRow.count("1")

	return cmp(count0, count1)


def filterBits(bitStrings: set[str], pos: int, expected: int) -> set[str]:
	filtered = {bitString for bitString in bitStrings if bitString[pos] == str(expected)}
	try:
		filtered.remove(None)
	except KeyError:
		pass
	finally:
		return filtered


def part2(inp: str) -> int:
	lines = tuple(line for line in inp.splitlines())
	bits0 = filterBits(set(lines), 0, 0)
	bits1 = filterBits(set(lines), 0, 1)

	if len(bits0) > len(bits1):
		oxygen = bits0
		co2 = bits1
	elif len(bits0) < len(bits1):
		oxygen = bits1
		co2 = bits0
	else:
		oxygen = bits1
		co2 = bits0

	for i in range(1, len(lines[0])):
		if len(oxygen) > 1:
			oxygen = filterBits(oxygen, i, {-1: 1, 0: 1, 1: 0}[mostCommon(oxygen, i)])
		if len(co2) > 1:
			co2 = filterBits(co2, i, {-1: 0, 0: 0, 1: 1}[mostCommon(co2, i)])

	oxygenS = "".join(oxygen)
	co2S = "".join(co2)

	return int(oxygenS, 2) * int(co2S, 2)


def main() -> int:
	inputPath = os.path.join(os.path.dirname(__file__), "input.txt")
	with open(inputPath) as inpF:
		inp = inpF.read().strip()
		print(f"Part 1: {part1(inp)}")
		print(f"Part 2: {part2(inp)}")
	return 0


EXAMPLE_INPUT = """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
""".strip()


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 198),
	),
)
def testPart1(inp: str, expected: int):
	assert part1(inp) == expected


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 230),
	),
)
def testPart2(inp: str, expected: int):
	assert part2(inp) == expected


if __name__ == "__main__":
	raise SystemExit(main())
