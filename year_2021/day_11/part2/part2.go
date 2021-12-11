package main

import (
	"fmt"
	"os"
	day11 "year_2021/day_11"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	octopuses := day11.ReadInput(os.Args[1])

	// Print
	fmt.Printf("Before any steps\n")
	for i := range octopuses {
		row := octopuses[i]
		for j := range row {
			fmt.Printf("%v", row[j])
		}
		fmt.Print("\n")
	}
	fmt.Print("\n")

	steps := 2000
	numFlashes := 0
	// For each step
	for step := 1; step <= steps; step++ {
		// Increase every octopus level by 1
		for i := range octopuses {
			row := octopuses[i]
			for j := range row {
				row[j] += 1
			}
		}

		// Check for flashes, recurse if there is one
		for j := range octopuses {
			row := octopuses[j]
			for i := range row {
				if row[i] > 9 {
					// Flash and affect neighbors
					numFlashes += day11.Flash(octopuses, i, j)
				}
			}
		}
		// Print and check if they have all flashed!
		allFlash := true
		fmt.Printf("After step %v: \n", step)
		for i := range octopuses {
			row := octopuses[i]
			for j := range row {
				if row[j] != 0 {
					allFlash = false
				}
				fmt.Printf("%v", row[j])
			}
			fmt.Print("\n")
		}
		fmt.Print("\n")
		// Stop if they all flashed
		if allFlash {
			fmt.Printf("ALL FLASHED step: %v\n", step)
			break
		}
	}

	fmt.Printf("Total flashes: %v\n", numFlashes)
}
