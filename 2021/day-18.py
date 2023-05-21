#!/usr/bin/env python3

from __future__ import annotations

import ast
import math
import os
import re

import pytest

PAT_PAIR = re.compile(r"\[(\d+),(\d+)\]")
PAT_BIGN = re.compile(r"\d\d+")


def addPair(p1: str, p2: str) -> str:
	return f"[{p1},{p2}]"


def reduce(s: str) -> str:
	while True:
		for pair in PAT_PAIR.finditer(s):
			# find explode
			prev = s[:pair.start()]
			if prev.count("[") - prev.count("]") >= 4:
				def nextLeft(m: re.Match[str]) -> str:
					return str(int(m[0]) + int(pair[1]))

				def nextRight(m: re.Match[str]) -> str:
					return str(int(m[0]) + int(pair[2]))

				start = re.sub(r"\d+(?!.*\d)", nextLeft, s[:pair.start()], count=1)
				end = re.sub(r"\d+", nextRight, s[pair.end():], count=1)
				s = f"{start}0{end}"
				break
		else:
			# no explode, split!
			bigMatch = PAT_BIGN.search(s)
			if bigMatch is not None:
				def split(m: re.Match[str]) -> str:
					v = int(m[0])
					return f"[{v // 2},{math.ceil(v / 2)}]"

				s = PAT_BIGN.sub(split, s, count=1)
				continue
			else:
				# nothing to split, done!
				return s
		continue

	raise AssertionError("unreachable")


def getSum(s: str) -> int:
	def getVal(v: int | list):
		if isinstance(v, int):
			return v
		else:
			assert len(v) == 2
			return 3 * getVal(v[0]) + 2 * getVal(v[1])

	return getVal(ast.literal_eval(s))


def part1(inp: str) -> int:
	lines = inp.splitlines()

	line = lines.pop(0)
	while True:
		breakTop = False
		try:
			line = addPair(line, lines.pop(0))
		except IndexError:
			breakTop = True

		line = reduce(line)

		if breakTop:
			break

	return getSum(line)


def part2(inp: str) -> int:
	lines = inp.splitlines()
	maxMag = 0

	for i, line1 in enumerate(lines):
		for line2 in lines[(i + 1):]:
			maxMag = max(
				maxMag,
				getSum(reduce(addPair(line1, line2))),
				getSum(reduce(addPair(line2, line1))),
			)

	return maxMag


def main() -> int:
	inputPath = os.path.join(os.path.dirname(__file__), "input.txt")
	with open(inputPath) as inpF:
		inp = inpF.read().strip()
		print(f"Part 1: {part1(inp)}")
		print(f"Part 2: {part2(inp)}")
	return 0


EXAMPLE_INPUT_1 = "[[1,2],[[3,4],5]]"
EXAMPLE_INPUT_2 = "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
EXAMPLE_INPUT_3 = "[[[[1,1],[2,2]],[3,3]],[4,4]]"
EXAMPLE_INPUT_4 = "[[[[3,0],[5,3]],[4,4]],[5,5]]"
EXAMPLE_INPUT_5 = "[[[[5,0],[7,4]],[5,5]],[6,6]]"
EXAMPLE_INPUT_6 = "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"
EXAMPLE_INPUT_7 = """
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
""".strip()


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT_1, 143),
		pytest.param(EXAMPLE_INPUT_2, 1384),
		pytest.param(EXAMPLE_INPUT_3, 445),
		pytest.param(EXAMPLE_INPUT_4, 791),
		pytest.param(EXAMPLE_INPUT_5, 1137),
		pytest.param(EXAMPLE_INPUT_6, 3488),
		pytest.param(EXAMPLE_INPUT_7, 4140),
	),
)
def testPart1(inp: str, expected: int):
	assert part1(inp) == expected


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT_7, 3993),
	),
)
def testPart2(inp: str, expected: int):
	assert part2(inp) == expected


if __name__ == "__main__":
	raise SystemExit(main())
