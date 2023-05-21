#!/usr/bin/env python3

import os

import pytest


def part1(inp: str) -> int:
	numbersS, *boardsS = inp.split("\n\n")
	numbers = tuple(int(str(n).strip()) for n in numbersS.split(","))

	boards: list[list[int]] = list()

	for board in boardsS:
		_board = []
		for line in board.strip().splitlines():
			line = line.strip()
			for num in line.split(" "):
				if num != "":
					_board.append(int(num.strip()))
		boards.append(_board)

	for number in numbers:
		for board in boards:
			if number in board:
				board[board.index(number)] = None
			for i in range(5):
				if board[(i * 5):((i * 5) + 5)] == [None] * 5:
					return number * sum(value for value in board if value is not None)
				else:
					rotated = list(board[(j * 5) + i] for i in range(5) for j in range(5))
					if rotated[(i * 5):((i * 5) + 5)] == [None] * 5:
						return number * sum(value for value in board if value is not None)

	raise AssertionError("unreachable")


# slightly cheated. explaination was kinda wanky and I couldn't find a way to make it work
def part2(inp: str) -> int:
	numbersS, *boardsS = inp.split("\n\n")
	numbers = tuple(int(str(n).strip()) for n in numbersS.split(","))

	boards: list[list[int]] = []

	for board in boardsS:
		_board = []
		for line in board.strip().splitlines():
			line = line.strip()
			for num in line.split(" "):
				if num != "":
					_board.append(int(num.strip()))
		boards.append(_board)

	seen: set[int] = set()
	lastWonScore = -1
	for number in numbers:
		for boardI, board in enumerate(boards):
			if len(boards) == 0:
				break

			if number in board:
				board[board.index(number)] = None

			for i in range(5):
				if board[(i * 5):((i * 5) + 5)] == [None] * 5 and boardI not in seen:
					seen.add(boardI)
					lastWonScore = number * sum(value for value in board if value is not None)
				else:
					rotated = list(board[(j * 5) + i] for i in range(5) for j in range(5))
					if rotated[(i * 5):((i * 5) + 5)] == [None] * 5 and boardI not in seen:
						seen.add(boardI)
						lastWonScore = number * sum(value for value in board if value is not None)

	return lastWonScore


def main() -> int:
	inputPath = os.path.join(os.path.dirname(__file__), "input.txt")
	with open(inputPath) as inpF:
		inp = inpF.read().strip()
		print(f"Part 1: {part1(inp)}")
		print(f"Part 2: {part2(inp)}")
	return 0


EXAMPLE_INPUT = """
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
8  2 23  4 24
21  9 14 16  7
6 10  3 18  5
1 12 20 15 19

3 15  0  2 22
9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
2  0 12  3  7
""".strip()


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 4512),
	),
)
def testPart1(inp: str, expected: int):
	assert part1(inp) == expected


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 1924),
	),
)
def testPart2(inp: str, expected: int):
	assert part2(inp) == expected


if __name__ == "__main__":
	raise SystemExit(main())
