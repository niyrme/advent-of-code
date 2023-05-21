#!/usr/bin/env python3

import os

import pytest


def part1(inp: str) -> int:
	x = 0
	depth = 0

	for command in inp.splitlines():
		cmd, value = str(command).lower().split(" ")
		_value = int(value)
		if cmd == "forward":
			x += _value
		elif cmd == "down":
			depth += _value
		elif cmd == "up":
			depth -= _value
	return x * depth


def part2(inp: str) -> int:
	x = 0
	depth = 0
	aim = 0

	for command in inp.splitlines():
		cmd, value = str(command).lower().split(" ")
		_value = int(value)
		if cmd == "forward":
			x += _value
			depth += aim * _value
		elif cmd == "down":
			aim += _value
		elif cmd == "up":
			aim -= _value
	return x * depth


def main() -> int:
	inputPath = os.path.join(os.path.dirname(__file__), "input.txt")
	with open(inputPath) as inpF:
		inp = inpF.read().strip()
		print(f"Part 1: {part1(inp)}")
		print(f"Part 2: {part2(inp)}")
	return 0


EXAMPLE_INPUT = """
forward 5
down 5
forward 8
up 3
down 8
forward 2
""".strip()


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 150),
	),
)
def testPart1(inp: str, expected: int):
	assert part1(inp) == expected


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 900),
	),
)
def testPart2(inp: str, expected: int):
	assert part2(inp) == expected


if __name__ == "__main__":
	raise SystemExit(main())
