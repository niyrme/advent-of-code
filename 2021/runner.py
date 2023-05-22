#!/usr/bin/env python3

import argparse
import os
import sys

import pytest


class Args:
	day: int
	runTests: bool


def main() -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument("day", type=int)
	parser.add_argument("-t", "--tests", action="store_true", dest="runTests")

	args = Args()
	parser.parse_args(namespace=args)

	if not 0 < args.day < 26:
		print(f"day must be in range 1-25, got {args.day}", file=sys.stderr)
		return 1

	dayName = f"day-{args.day:>02}.py"

	if dayName not in os.listdir(os.path.dirname(__file__)):
		print(f"day {args.day} not found", file=sys.stderr)
		return 1

	if args.runTests is True:
		if (testRet := pytest.main([dayName, "-q"])) not in (pytest.ExitCode.OK, pytest.ExitCode.NO_TESTS_COLLECTED):
			print(f"day {args.day} tests failed with exit code {int(testRet)}", file=sys.stderr)
			return int(testRet)
	else:
		with open(dayName, "r") as script:
			exec(script.read())

	return 0


if __name__ == "__main__":
	raise SystemExit(main())
