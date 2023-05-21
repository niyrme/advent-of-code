#!/usr/bin/env python3

from __future__ import annotations

import os
from math import prod
from typing import NamedTuple

import pytest


# code mostly stolen from here:
# https://github.com/anthonywritescode/aoc2021/tree/ee6276a00978e8a30e571233e85e78d3d59dd9e7/day16
# because sometimes I'm not smort and it's 7AM with 4 hrs of sleep


class Packet(NamedTuple):
	ver: int
	typID: int
	val: int = -1
	packets: tuple[Packet, ...] = tuple()


def parsePacket(bitS, i: int) -> tuple[int, Packet]:
	def read(n: int) -> int:
		nonlocal i
		ret = int(bitS[i:i + n], 2)
		i += n
		return ret

	packVer = read(3)
	packTypID = read(3)

	if packTypID == 4:
		packVal = 0
		chunk = read(5)
		packVal += chunk & 0b1111
		while chunk & 0b10000:
			chunk = read(5)
			packVal <<= 4
			packVal += chunk & 0b1111

		return i, Packet(
			ver=packVer,
			typID=packTypID,
			val=packVal,
		)
	else:
		op = read(1)
		if op == 0:
			packsLen = read(15)
			j = i
			i += packsLen
			packs = []
			while j < i:
				j, packet = parsePacket(bitS, j)
				packs.append(packet)

			return i, Packet(
				ver=packVer,
				typID=packTypID,
				packets=tuple(packs),
			)
		else:
			subPacks = read(11)
			packs = []
			for _ in range(subPacks):
				i, packet = parsePacket(bitS, i)
				packs.append(packet)

			return i, Packet(
				ver=packVer,
				typID=packTypID,
				packets=tuple(packs),
			)


def part1(inp: str) -> int:
	bitS = "".join(f"{int(hx, 16):04b}" for hx in inp.strip())
	total = 0
	todo = [parsePacket(bitS, 0)[1]]
	while todo:
		nextP = todo.pop()
		total += nextP.ver
		todo.extend(nextP.packets)

	return total


def part2(inp: str) -> int:
	def getVal(packet: Packet) -> int:
		if packet.typID in (0, 1, 2, 3):
			return {
				0: sum,
				1: prod,
				2: min,
				3: max,
			}[packet.typID](getVal(subP) for subP in packet.packets)
		elif packet.typID == 4:
			return packet.val
		elif packet.typID == 5:
			return int(getVal(packet.packets[0]) > getVal(packet.packets[1]))
		elif packet.typID == 6:
			return int(getVal(packet.packets[0]) < getVal(packet.packets[1]))
		elif packet.typID == 7:
			return int(getVal(packet.packets[0]) == getVal(packet.packets[1]))
		else:
			raise AssertionError("unreachable", packet)

	bitS = "".join(f"{int(hx, 16):04b}" for hx in inp.strip())
	return getVal(parsePacket(bitS, 0)[1])


def main() -> int:
	inputPath = os.path.join(os.path.dirname(__file__), "input.txt")
	with open(inputPath) as inpF:
		inp = inpF.read().strip()
		print(f"Part 1: {part1(inp)}")
		print(f"Part 2: {part2(inp)}")
	return 0


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param("8A004A801A8002F478", 16),
		pytest.param("620080001611562C8802118E34", 12),
		pytest.param("C0015000016115A2E0802F182340", 23),
		pytest.param("A0016C880162017C3686B18A3D4780", 31),
	),
)
def testPart1(inp: str, expected: int):
	assert part1(inp) == expected


@pytest.mark.parametrize(
	("inp", "expected"), (
		pytest.param("C200B40A82", 3),
		pytest.param("04005AC33890", 54),
		pytest.param("880086C3E88112", 7),
		pytest.param("CE00C43D881120", 9),
		pytest.param("D8005AC2A8F0", 1),
		pytest.param("F600BC2D8F", 0),
		pytest.param("9C005AC2F8F0", 0),
		pytest.param("9C0141080250320F1802104A08", 1),
	),
)
def testPart2(inp: str, expected: int):
	assert part2(inp) == expected


if __name__ == "__main__":
	raise SystemExit(main())
