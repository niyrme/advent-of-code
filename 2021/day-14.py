#!/usr/bin/env python3

import os
from collections import Counter

import pytest


def calc(templ: str, _patterns: str, iters: int) -> int:
	patterns = dict()
	for pattern in _patterns.splitlines():
		frm, to = pattern.split(" -> ")
		patterns[frm] = to

	pairCounts = Counter()
	for i in range(len(templ) - 1):
		pairCounts[templ[i:i + 2]] += 1

	charCounts = Counter()

	for _ in range(iters):
		newPairs = Counter()
		charCounts = Counter()

		for k, v in pairCounts.items():
			pat = patterns[k]
			newPairs[f"{k[0]}{pat}"] += v
			newPairs[f"{pat}{k[1]}"] += v

			charCounts[k[0]] += v
			charCounts[pat] += v

		pairCounts = newPairs

	charCounts[templ[-1]] += 1

	return max(charCounts.values()) - min(charCounts.values())


def part1(inp: str) -> int:
	return calc(*inp.split("\n\n"), iters=10)


def part2(inp: str) -> int:
	return calc(*inp.split("\n\n"), iters=40)


def main() -> int:
	inputPath = os.path.join(os.path.dirname(__file__), "input.txt")
	with open(inputPath) as inpF:
		inp = inpF.read().strip()
		print(f"Part 1: {part1(inp)}")
		print(f"Part 2: {part2(inp)}")
	return 0


EXAMPLE_INPUT = """
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
""".strip()


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 1588),
	),
)
def testPart1(inp: str, expected: int):
	assert part1(inp) == expected


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 2188189693529),
	),
)
def testPart2(inp: str, expected: int):
	assert part2(inp) == expected


if __name__ == "__main__":
	raise SystemExit(main())
