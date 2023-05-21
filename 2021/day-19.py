#!/usr/bin/env python3
from __future__ import annotations

import os
from collections import Counter
from typing import Literal
from typing import NamedTuple

import pytest


class Scanner(NamedTuple):
	id_: int
	points: list[tuple[int, int, int]]

	@classmethod
	def fromStr(cls, s: str) -> Scanner:
		lines = s.splitlines()

		id_ = int(lines[0][12:][:-4])
		points = []
		for line in lines[1:]:
			xS, yS, zS = line.split(",")
			points.append((int(xS), int(yS), int(zS)))
		return cls(id_, points)


class AxisInfo(NamedTuple):
	axis: Literal[0, 1, 2]
	sign: Literal[-1, 1]
	diff: int


def xEdgesFrom(src: Scanner, scannersID: dict[int, Scanner]) -> dict[int, AxisInfo]:
	xEdges = dict()
	for other in scannersID.values():
		for axis in (0, 1, 2):
			for sign in (-1, 1):
				dX = Counter()
				for x, _, _ in src.points:
					for otherPt in other.points:
						dX[x - otherPt[axis] * sign] += 1

				(xDiff, n), = dX.most_common(1)
				if n >= 12:
					xEdges[other.id_] = AxisInfo(axis, sign, xDiff)

	return xEdges


def yzEdgesFrom(src: Scanner, xEdges: dict[int, AxisInfo], scannersID: dict[int, Scanner]) -> tuple[dict[int, AxisInfo], dict[int, AxisInfo]]:
	yEdges = dict()
	zEdges = dict()
	for dstID in xEdges:
		other = scannersID[dstID]
		for axis in (0, 1, 2):
			for sign in (-1, 1):
				dY = Counter()
				dZ = Counter()
				for _, y, z in src.points:
					for otherPt in other.points:
						dY[y - otherPt[axis] * sign] += 1
						dZ[z - otherPt[axis] * sign] += 1

				(yDiff, yN), = dY.most_common(1)
				if yN >= 12:
					yEdges[dstID] = AxisInfo(axis, sign, yDiff)

				(zDiff, zN), = dZ.most_common(1)
				if zN >= 12:
					zEdges[dstID] = AxisInfo(axis, sign, zDiff)

	return (yEdges, zEdges)


def part1(inp: str) -> int:
	scanners = list(Scanner.fromStr(scan) for scan in inp.split("\n\n"))
	scannersID = {s.id_: s for s in scanners}
	scannerPos = {0: (0, 0, 0)}
	points = set(scannersID[0].points)

	todo = [scannersID.pop(0)]
	while todo:
		src = todo.pop()

		xEdges = xEdgesFrom(src, scannersID)
		yEdges, zEdges = yzEdgesFrom(src, xEdges, scannersID)

		for k in xEdges:
			dstX = xEdges[k].diff
			dstY = yEdges[k].diff
			dstZ = zEdges[k].diff

			scannerPos[k] = (dstX, dstY, dstZ)

			nextScanner = scannersID.pop(k)
			nextScanner.points[:] = [
				(
					dstX + xEdges[k].sign * pt[xEdges[k].axis],
					dstY + yEdges[k].sign * pt[yEdges[k].axis],
					dstZ + zEdges[k].sign * pt[zEdges[k].axis],
				)
				for pt in nextScanner.points
			]
			points.update(nextScanner.points)
			todo.append(nextScanner)

	return len(points)


def part2(inp: str) -> int:
	scanners = list(Scanner.fromStr(scan) for scan in inp.split("\n\n"))
	scannersID = {s.id_: s for s in scanners}
	scannerPos = {0: (0, 0, 0)}
	points = set(scannersID[0].points)

	todo = [scannersID.pop(0)]
	while todo:
		src = todo.pop()

		xEdges = xEdgesFrom(src, scannersID)
		yEdges, zEdges = yzEdgesFrom(src, xEdges, scannersID)

		for k in xEdges:
			dstX = xEdges[k].diff
			dstY = yEdges[k].diff
			dstZ = zEdges[k].diff

			scannerPos[k] = (dstX, dstY, dstZ)

			nextScanner = scannersID.pop(k)
			nextScanner.points[:] = [
				(
					dstX + xEdges[k].sign * pt[xEdges[k].axis],
					dstY + yEdges[k].sign * pt[yEdges[k].axis],
					dstZ + zEdges[k].sign * pt[zEdges[k].axis],
				)
				for pt in nextScanner.points
			]
			points.update(nextScanner.points)
			todo.append(nextScanner)

	maxDist = 0
	poss = list(scannerPos.values())
	for i, (x1, y1, z1) in enumerate(poss):
		for x2, y2, z2 in poss[i:]:
			maxDist = max(maxDist, abs(x2 - x1) + abs(y2 - y1) + abs(z2 - z1))

	return maxDist


def main() -> int:
	inputPath = os.path.join(os.path.dirname(__file__), "input.txt")
	with open(inputPath) as inpF:
		inp = inpF.read().strip()
		print(f"Part 1: {part1(inp)}")
		print(f"Part 2: {part2(inp)}")
	return 0


EXAMPLE_INPUT = """
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
""".strip()


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 79),
	),
)
def testPart1(inp: str, expected: int):
	assert part1(inp) == expected


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param(EXAMPLE_INPUT, 3621),
	),
)
def testPart2(inp: str, expected: int):
	assert part2(inp) == expected


if __name__ == "__main__":
	raise SystemExit(main())
