package main

import (
	"fmt"
	"math"
	"os"
	"sort"
	day07 "year_2021/day_07"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	crabs := day07.ReadInput(os.Args[1])
	sort.Ints(crabs)
	// fmt.Printf("Input: %v\n", crabs)
	maxDist := crabs[len(crabs)-1]
	// fmt.Printf("Max dist: %v\n", maxDist)

	minCost := 9999999
	// For each possible distance, compute the cost
	for dist := 0; dist < maxDist; dist++ {
		cost := 0
		tooExpensive := false
		for _, crab := range crabs {
			cost += int(math.Abs(float64(dist - crab)))
			if cost > minCost {
				tooExpensive = true
				break
			}
		}
		if !tooExpensive && cost < minCost {
			minCost = cost
		}
		// fmt.Printf("Dist: %v, Cost: %v\n", dist, cost)
	}

	fmt.Printf("Min cost: %v\n", minCost)
}
