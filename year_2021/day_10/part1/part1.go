package main

import (
	"fmt"
	"os"
	day10 "year_2021/day_10"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	lines := day10.ReadInput(os.Args[1])
	fmt.Printf("Input: %v\n", lines)

	lookup := map[rune]int{
		')': 3,
		']': 57,
		'}': 1197,
		'>': 25137,
	}

	points := 0
	// For each line, find corrupted lines
	for i, line := range lines {
		err, char, _ := day10.CheckLineSyntax(line)
		if err != nil {
			fmt.Printf("%v: %v - %v\n", i, line, err)
			points += lookup[char]
		}
	}

	fmt.Printf("Result: %v\n", points)
}
