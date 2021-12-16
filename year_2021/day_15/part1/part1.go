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

	start := utils.Coord{I: 0, J: 0}
	end := utils.Coord{I: len(grid) - 1, J: len(grid[0]) - 1}

	cost := day15.Astar(grid, start, end)

	fmt.Printf("\nend cost: %v\n", cost[end])
}
