package main

import (
	"fmt"
	"os"
)

type Day struct {
	inputFile string
	part1     func(input string) string
	part2     func(input string) string
}

func (d Day) Run() error {
	bytes, err := os.ReadFile(d.inputFile)

	if err != nil {
		return err
	}

	input := string(bytes)

	fmt.Printf("Part 1: %v\n", d.part1(input))
	fmt.Printf("Part 2: %v\n", d.part2(input))

	return nil
}
