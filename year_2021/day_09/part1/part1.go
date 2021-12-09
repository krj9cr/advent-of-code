package main

import (
	"fmt"
	"os"
	day09 "year_2021/day_09"
	"year_2021/utils"
)

// Returns list of neighbor values (not coords)
func getNeighbors(grid [][]int, i int, j int) []int {
	up := j - 1
	down := j + 1
	left := i - 1
	right := i + 1
	height := len(grid)
	width := len(grid[0])

	var neighbors []int
	if up >= 0 {
		neighbors = append(neighbors, grid[up][i])
	}
	if left >= 0 {
		neighbors = append(neighbors, grid[j][left])
	}
	if down < height {
		neighbors = append(neighbors, grid[down][i])
	}
	if right < width {
		neighbors = append(neighbors, grid[j][right])
	}
	return neighbors
}

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	grid := day09.ReadInput(os.Args[1])
	utils.PrintIntGrid(grid)

	sum := 0
	for j, row := range grid {
		for i, item := range row {
			isLowPoint := true
			neighbors := getNeighbors(grid, i, j)
			// fmt.Printf("Item: %v at (%v,%v)\n has neighbors: %v\n", item, i, j, neighbors)
			for _, n := range neighbors {
				if n <= item {
					isLowPoint = false
					break
				}
			}
			if isLowPoint {
				fmt.Printf("Item: %v at (%v,%v) is low with neighbors: %v\n", item, i, j, neighbors)
				sum += item + 1
			}
		}
	}
	// 1442 too high

	fmt.Printf("Result: %v\n", sum)
}
