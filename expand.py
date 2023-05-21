#!/usr/bin/env python3

import argparse
import os
import pathlib
import re
import shutil
import sys


class Args:
	day: int
	year: int


def addDay(year: str, day: int):
	dayStr = f"{day:>02}"

	print(f"Adding {year}/{dayStr}")

	templateReg = re.compile(r"^template.*?\.([^\.]+)$")

	template = tuple(filter(
		lambda f: templateReg.match(f) is not None,
		os.listdir(year)
	))[0]

	ext: str = templateReg.match(template)[1]

	outPath = os.path.join(year, f"day-{dayStr}.{ext}")

	if os.path.exists(outPath):
		try:
			while True:
				match (input(f"File '{outPath}' already exists. Overwrite? ").strip().lower()):
					case "y" | "yes": break
					case "n" | "no": return
					case _: print("Invalid option", file=sys.stderr)
		except KeyboardInterrupt:
			return

	shutil.copy(
		os.path.join(year, template),
		outPath,
	)


def main() -> int:
	args = Args()
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-d", "--day",
		action="store",
		type=int,
		dest="day",
	)
	parser.add_argument(
		"-y", "--year",
		action="store",
		type=int,
		dest="year",
	)

	parser.parse_args(namespace=args)

	if args.year:
		year = args.year
	else:
		year = max((int(year_.name) for year_ in pathlib.Path(".").iterdir() if year_.name.isnumeric()))

	if args.day:
		day = args.day
	else:
		dayReg = re.compile(r"^day-(\d+)")
		days = [-1]

		for day_ in pathlib.Path(f"./{year}").iterdir():
			m = dayReg.match(day_.name)
			if m is None:
				continue
			days.append(int(m[1]))

		day = max(days) + 1

	if not 0 < day < 26:
		print(f"AoC only has days 1-25. Given day: {day}", file=sys.stderr)
		return 1

	print(day)

	addDay(str(year), day)

	return 0


if __name__ == "__main__":
	raise SystemExit(main())
