package main

import (
	"fmt"
	"os"
	day14 "year_2021/day_14"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	start, polymers := day14.ReadInput(os.Args[1])
	// fmt.Printf("Input: %v, polymers: %v\n", start, polymers)

	curr := start
	steps := 40 // should be 10
	for step := 1; step <= steps; step++ {
		var updatedPairs []string
		// Iterate through pairs
		for i := range curr {
			if i+1 < len(curr) {
				pair := curr[i : i+2]
				// fmt.Printf("pair: %v\n", pair)
				// see if any polymers match
				for _, polymer := range polymers {
					if polymer.Pair == pair {
						// fmt.Printf("matching poly: %v\n", polymer)
						// Add to updated list
						updatedPairs = append(updatedPairs, string(pair[0])+polymer.Insert+string(pair[1]))
					}
				}
			}
		}
		// Join list of updated pairs
		// fmt.Printf("Updated pairs: %v\n", updatedPairs)
		curr = ""
		for i, pair := range updatedPairs {
			if i == 0 {
				curr += string(pair[0]) + string(pair[1])
			} else if i == len(updatedPairs)-1 {
				curr += pair
			} else {
				curr += string(pair[0]) + string(pair[1])
			}
		}
		// fmt.Printf("After step %v: length: %v; %v\n", step, len(curr), curr)
	}

	// Count letters
	counts := make(map[rune]int, 0)
	for _, char := range curr {
		counts[char] += 1
	}
	maxc := 0
	minc := 999999999
	for _, val := range counts {
		if val > maxc {
			maxc = val
		}
		if val < minc {
			minc = val
		}
	}

	// fmt.Printf("Counts: %v\n", counts)
	fmt.Printf("Result: %v - %v = %v", maxc, minc, maxc-minc)
}
