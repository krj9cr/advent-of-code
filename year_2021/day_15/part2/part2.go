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

	w := len(grid[0])

	multiplier := 4
	// expand board for part2 horizontally
	var bigBoard [][]int
	for _, row := range grid {
		var newRow []int
		for s := 0; s <= multiplier; s++ {
			for i := 0; i < w; i++ {
				item := row[i]
				newItem := item + s
				if newItem > 9 {
					newItem = newItem - 9
				}
				newRow = append(newRow, newItem)
			}
		}
		bigBoard = append(bigBoard, newRow)
	}

	// expand board vertically
	grid = bigBoard
	var newRows [][]int
	for s := 1; s <= multiplier; s++ {
		for _, row := range grid {
			var newRow []int
			for i := 0; i < len(grid[0]); i++ {
				item := row[i]
				newItem := item + s
				if newItem > 9 {
					newItem = newItem - 9
				}
				newRow = append(newRow, newItem)
			}
			newRows = append(newRows, newRow)
		}
	}
	grid = append(grid, newRows...)

	utils.PrintIntGrid(grid)

	start := utils.Coord{I: 0, J: 0}
	end := utils.Coord{I: len(grid) - 1, J: len(grid[0]) - 1}

	cost := day15.Astar(grid, start, end)

	fmt.Printf("\nend cost: %v\n", cost[end])
}
