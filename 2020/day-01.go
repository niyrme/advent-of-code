package main

import (
	"fmt"
	"log"
	"strconv"
	"strings"
)

var Day01 Day = Day{
	inputFile: "./inputs/01.txt",
	part1: func(input string) string {
		input = strings.Trim(input, " \n\r\t")
		lines := strings.Split(input, "\n")

		var nums []int

		for _, line := range lines {
			if n, err := strconv.Atoi(line); err != nil {
				log.Fatalln(err)
			} else {
				nums = append(nums, n)
			}
		}

		for _, i := range nums {
			for _, j := range nums {
				if i+j == 2020 {
					return fmt.Sprintf("%d", i*j)
				}
			}
		}

		log.Fatalln("unreachable")
		return ""
	},
	part2: func(input string) string {
		input = strings.Trim(input, " \n\r\t")
		lines := strings.Split(input, "\n")

		var nums []int

		for _, line := range lines {
			if n, err := strconv.Atoi(line); err != nil {
				log.Fatalln(err)
			} else {
				nums = append(nums, n)
			}
		}

		for _, i := range nums {
			for _, j := range nums {
				for _, k := range nums {
					if i+j+k == 2020 {
						return fmt.Sprintf("%d", i*j*k)
					}
				}
			}
		}

		log.Fatalln("unreachable")
		return ""
	},
}
