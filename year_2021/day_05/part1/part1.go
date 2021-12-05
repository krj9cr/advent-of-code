package main

import (
	"fmt"
	"os"
	day05 "year_2021/day_05"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	lines := day05.ReadInput(os.Args[1])
	fmt.Printf("Input: %v\n", lines)

	_, maxx, _, maxy := day05.FindMinMaxCoords(lines)

	fmt.Printf("maxx: %v, maxy: %v", maxx, maxy)
	grid := make([][]int, maxx+2)
	for i := range grid {
		grid[i] = make([]int, maxy+2)
	}

	// utils.PrintGrid(grid)

	for _, line := range lines {
		line.Chart(grid, false)
	}
	// utils.PrintGrid(grid)

	count := 0
	for _, row := range grid {
		for _, item := range row {
			if item > 1 {
				count += 1
			}
		}
	}

	fmt.Printf("Result: %v\n", count)

	//15413 too high
	//15284 too high
}
