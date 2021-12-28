package main

import (
	"fmt"
	"os"
	"sort"
	day10 "year_2021/day_10"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	lines := day10.ReadInput(os.Args[1])
	// fmt.Printf("Input: %v\n", lines)

	lookup := map[rune]int{
		')': 1,
		']': 2,
		'}': 3,
		'>': 4,
	}

	var scores []int
	// For each line, find corrupted lines
	for _, line := range lines {
		err, _, stack := day10.CheckLineSyntax(line)
		if err != nil && fmt.Sprint(err) == "stack still contains values" {

			runes := day10.AutocompleteStack(stack)
			score := 0
			for _, r := range runes {
				score = (score * 5) + lookup[r]
			}

			// fmt.Printf("%v: %v - %v: ", i, line, err)
			// for _, s := range runes {
			// 	fmt.Printf("%v", string(s))
			// }
			// fmt.Printf(" score: %v\n", score)
			scores = append(scores, score)
		}
	}

	sort.Ints(scores)
	// fmt.Printf("Scores: %v\n", scores)
	fmt.Printf("Result: %v\n", scores[len(scores)/2])

}
