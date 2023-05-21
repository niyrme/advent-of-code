#!/usr/bin/env python3

import os

import pytest


def part1(inp: str) -> int:
	penalty = {
		")": 3,
		"]": 57,
		"}": 1197,
		">": 25137,
	}

	closeToOpen = {
		")": "(",
		"]": "[",
		"}": "{",
		">": "<",
	}

	total = 0
	for line in inp.splitlines():
		opened = []

		for c in line:
			if c in "([{<":
				opened.append(c)
			elif c in ")]}>":
				if opened.pop() != closeToOpen[c]:
					total += penalty[c]
	return total


def part2(inp: str) -> int:
	penalty = {k: i + 1 for i, k in enumerate("([{<")}

	closeToOpen = {
		")": "(",
		"]": "[",
		"}": "{",
		">": "<",
	}

	totals = []
	for line in inp.splitlines():
		opened = []

		for c in line:
			if c in "([{<":
				opened.append(c)
			elif c in ")]}>":
				if opened.pop() != closeToOpen[c]:
					break
		else:
			score = 0
			for o in reversed(opened):
				score = (score * 5) + penalty[o]

			totals.append(score)

	totals.sort()
	return totals[len(totals) // 2]


def main() -> int:
	inputPath = os.path.join(os.path.dirname(__file__), "input.txt")
	with open(inputPath) as inpF:
		inp = inpF.read().strip()
		print(f"Part 1: {part1(inp)}")
		print(f"Part 2: {part2(inp)}")
	return 0


EXAMPLE_INPUT = """
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
""".strip()


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 26397),
	),
)
def testPart1(inp: str, expected: int):
	assert part1(inp) == expected


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 288957),
	),
)
def testPart2(inp: str, expected: int):
	assert part2(inp) == expected


if __name__ == "__main__":
	raise SystemExit(main())
