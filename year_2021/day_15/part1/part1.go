package main

import (
	"fmt"
	"os"
	day15 "year_2021/day_15"
	"year_2021/utils"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	grid := utils.ReadLinesToIntGrid(os.Args[1], "")
	utils.PrintIntGrid(grid)

	start := day15.Coord{0, 0}
	end := day15.Coord{len(grid) - 1, len(grid[0]) - 1}

	cameFrom, cost := day15.Astar(grid, start, end)

	// Figure out the path
	curr := end
	fmt.Printf("Path?: %v ", curr)
	for {
		next, ok := cameFrom[curr]
		if next == nil || !ok {
			break
		}
		curr = *next
		fmt.Printf("%v ", curr)
	}

	fmt.Printf("\nend cost: %v\n", cost[end])
}
