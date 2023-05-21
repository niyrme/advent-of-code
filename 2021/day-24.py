#!/usr/bin/env python3
from __future__ import annotations

import operator
import os
from typing import Any
from typing import Union

import z3


class Expr:
	def __init__(self, left: Union[int, Expr, Var], op: str, right: Union[int, Expr, Var]) -> None:
		self._left = left
		self._op = op
		self._right = right

	def __repr__(self) -> str:
		return f"{self.__class__.__name__}(left={self.left!r}, op={self.op}, right={self.right!r})"

	def __add__(self, other) -> Expr:
		if other == 0:
			return self
		elif isinstance(other, (int, Expr, Var)):
			return type(self)(self, "+", other)
		else:
			raise AssertionError("unexpected add", other, self)

	__radd__ = __add__

	def __mul__(self, other) -> Union[int, Expr]:
		if other == 0:
			return 0
		elif other == 1:
			return self
		elif isinstance(other, (int, Expr)):
			return type(self)(self, "*", other)
		else:
			raise AssertionError("unexpected mul", other, self)

	__rmul__ = __mul__

	def __floordiv__(self, other) -> Expr:
		if other == 1:
			return self
		elif isinstance(other, (int, Expr)):
			return type(self)(self, "//", other)
		else:
			raise AssertionError("unexpected floordiv", other, self)

	def __mod__(self, other) -> Expr:
		if isinstance(other, (int, Expr)):
			return type(self)(self, "%", other)
		else:
			raise AssertionError("unexpected mod", other, self)

	def __eq__(self, other) -> bool:
		if isinstance(other, int):
			assert other in (0, 1), other
			return False
		assert self.op == "+"
		assert isinstance(self.right, int), self.right
		assert self.right < 1 or self.right >= 10
		assert isinstance(other, Var)
		return False

	@property
	def left(self):
		return self._left

	@property
	def right(self):
		return self._right

	@property
	def op(self):
		return self._op


class Var:
	def __init__(self, value: int) -> None:
		self.value = value

	def __repr__(self) -> str:
		return f"{self.__class__.__name__}({self.value})"

	def __add__(self, other) -> Union[Var, Expr]:
		if other == 0:
			return self
		elif isinstance(other, (int, Expr)):
			return Expr(other, "+", self)
		else:
			raise AssertionError("unexpected add", other, self)

	__radd__ = __add__

	def __eq__(self, other) -> bool:
		if other is self:
			return True
		else:
			assert isinstance(other, int), (self, other)
			assert other < 1 or other >= 10
			return False

	def __mul__(self, other):
		return Expr(other, "*", self)


def compute(inp: str):
	registers: dict[str, Union[int, Expr, Var]] = {k: 0 for k in "xyz"}

	varW = Var(-1)

	def getVal(s: str) -> Union[int, Expr, Var]:
		if s == "w":
			return varW
		elif s.isalpha():
			return registers[s]
		else:
			return int(s)

	operators = {
		"+": operator.add,
		"*": operator.mul,
		"//": operator.truediv,
		"%": operator.mod,
	}

	numbers = [z3.Int(f"W_{i}") for i in range(14)]

	def toZ3(expr: Union[int, Expr, Var]) -> Any:
		if isinstance(expr, bool):
			return int(expr)
		elif isinstance(expr, int):
			return expr
		elif isinstance(expr, Var):
			return numbers[expr.value]
		else:
			return operators[expr.op](toZ3(expr.left), toZ3(expr.right))

	opt = z3.Optimize()
	for number in numbers:
		opt.add(number >= 1)
		opt.add(number < 10)

	for i, line in enumerate(inp.splitlines()):
		cmd = line.split()
		if cmd[0] == "inp":
			varW = Var(varW.value + 1)
		elif cmd[0] == "add":
			assert len(cmd) == 3
			if cmd[2].startswith("-"):
				opt.add(numbers[varW.value] == toZ3(registers["x"] + int(cmd[2])))
				registers["x"] = varW
			else:
				registers[cmd[1]] += getVal(cmd[2])
		elif cmd[0] == "mul":
			assert len(cmd) == 3
			if cmd[2] == "0":
				registers[cmd[1]] = 0
			else:
				registers[cmd[1]] *= getVal(cmd[2])
		elif cmd[0] == "div":
			assert len(cmd) == 3
			registers[cmd[1]] //= getVal(cmd[2])
		elif cmd[0] == "mod":
			assert len(cmd) == 3
			registers[cmd[1]] %= getVal(cmd[2])
		elif cmd[0] == "eql":
			assert len(cmd) == 3
			registers[cmd[1]] = (registers[cmd[1]] == getVal(cmd[2]))
		else:
			raise AssertionError(cmd)

	_sum = z3.Int("Sum")
	opt.add(_sum == sum(number * 10 ** (13 - i) for i, number in enumerate(numbers)))
	return opt, _sum


def part1(inp: str) -> int:
	opt, _sum = compute(inp)
	opt.maximize(_sum)
	assert opt.check() == z3.sat
	return opt.model()[_sum]


def part2(inp: str) -> int:
	opt, _sum = compute(inp)
	opt.minimize(_sum)
	assert opt.check() == z3.sat
	return opt.model()[_sum]


def main() -> int:
	inputPath = os.path.join(os.path.dirname(__file__), "input.txt")
	with open(inputPath) as inpF:
		inp = inpF.read().strip()
		print(f"Part 1: {part1(inp)}")
		print(f"Part 2: {part2(inp)}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
