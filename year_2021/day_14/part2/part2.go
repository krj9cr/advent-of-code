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
	fmt.Printf("Input: %v, polymers: %v\n", start, polymers)

	// convert polymers to a map
	polymersMap := make(map[string]string)
	for _, polymer := range polymers {
		polymersMap[polymer.Pair] = polymer.Insert
	}

	curr := start
	// create map of counts of letters
	letterCounts := make(map[string]int, 0)
	for _, char := range curr {
		letterCounts[string(char)] += 1
	}

	// create map of counts of pairs
	pairCounts := make(map[string]int, 0)
	// Iterate through pairs
	for i := range curr {
		if i+1 < len(curr) {
			pair := curr[i : i+2]
			pairCounts[pair] += 1
		}
	}

	steps := 40 // should be 40
	for step := 1; step <= steps; step++ {
		newPairCounts := make(map[string]int, 0)
		for pair, pairCount := range pairCounts {
			newPairCounts[pair] = pairCount
		}
		// Iterate through pairs
		for pair, pairCount := range pairCounts {
			//for p := 0; p < pairCount; p++ {
				// Find matching polymer
				if insert, ok := polymersMap[pair]; ok {
					// Update pair counts
					newPairCounts[pair] -= pairCount
					pairA := string(pair[0]) + insert
					pairB := insert + string(pair[1])
					newPairCounts[pairA] += pairCount
					newPairCounts[pairB] += pairCount
					// Add to letter counts
					letterCounts[insert] += pairCount
					//fmt.Printf("pair: %v; adding %v and %v\n", pair, pairA, pairB)
				}
			}
		//}
		pairCounts = newPairCounts
		// Sum letter counts to get length?
		length := 0
		for _, letterCount := range letterCounts {
			length += letterCount
		}
		fmt.Printf("After step %v: length: %v\n letterCounts: %v\n pairCounts: %v\n", step, length, letterCounts, pairCounts)
	}

	// Get max and min letter
	maxc := 0
	const MaxUint = ^uint(0)
	minc := int(MaxUint >> 1)
	for _, letterCount := range letterCounts {
		if letterCount > maxc {
			maxc = letterCount
		}
		if letterCount < minc {
			minc = letterCount
		}
	}

	fmt.Printf("Result: %v - %v = %v", maxc, minc, maxc-minc)
}
