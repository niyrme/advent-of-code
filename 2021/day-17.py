#!/usr/bin/env python3

import os

import pytest


def part1(inp: str) -> int:
	target = inp.strip()[13:]
	rangeY = target.split(", ")[1]

	startY = rangeY[2:].split("..")[0]

	y = abs(int(startY)) - 1
	return y * y - (y - 1) * y // 2


def part2(inp: str) -> int:
	target = inp.strip()[13:]
	rangeX, rangeY = target.split(", ")
	startXS, endXS = rangeX[2:].split("..")
	startYS, endYS = rangeY[2:].split("..")

	startX, endX = int(startXS), int(endXS)
	startY, endY = int(startYS), int(endYS)

	total = 0

	for x in range(1, endX + 1):
		for y in range(startY, abs(startY)):
			velX = x
			velY = y
			posX = posY = 0
			for _ in range(2 * abs(startY) + 1):
				posX += velX
				posY += velY

				if velX > 0:
					velX -= 1
				elif velX < 0:
					velX += 1

				velY -= 1

				if startX <= posX <= endX and startY <= posY <= endY:
					total += 1
					break
				elif posX > endX or posY < startY:
					# overshot the target
					break

	return total


def main() -> int:
	inputPath = os.path.join(os.path.dirname(__file__), "input.txt")
	with open(inputPath) as inpF:
		inp = inpF.read().strip()
		print(f"Part 1: {part1(inp)}")
		print(f"Part 2: {part2(inp)}")
	return 0


EXAMPLE_INPUT = "target area: x=20..30, y=-10..-5".strip()


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 45),
	),
)
def testPart1(inp: str, expected: int):
	assert part1(inp) == expected


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 112),
	),
)
def testPart2(inp: str, expected: int):
	assert part2(inp) == expected


if __name__ == "__main__":
	raise SystemExit(main())
