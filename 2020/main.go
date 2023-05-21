package main

import (
	"fmt"
	"os"

	"github.com/akamensky/argparse"
)

func main() {
	parser := argparse.NewParser("runner", "AoC 2020 runner")

	day_ := parser.IntPositional(&argparse.Options{Help: "Day to run"})

	if err := parser.Parse(os.Args); err != nil {
		fmt.Println(parser.Usage(err))
		return
	}

	day := *day_

	var runner Day
	switch day {
	case 1:
		runner = Day01
	case 2:
	case 3:
	case 4:
	case 5:
	case 6:
	case 7:
	case 8:
	case 9:
	case 10:
	case 11:
	case 12:
	case 13:
	case 14:
	case 15:
	case 16:
	case 17:
	case 18:
	case 19:
	case 20:
	case 21:
	case 22:
	case 23:
	case 24:
	case 25:
	default:
		fmt.Println(fmt.Errorf("day must be in range 1-25, got %d", day))
		return
	}

	if err := runner.Run(); err != nil {
		fmt.Println(err)
	}
}
