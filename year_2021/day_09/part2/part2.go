package main

import (
	"fmt"
	"os"
	"sort"
	day09 "year_2021/day_09"
	"year_2021/utils"
)


func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	grid := day09.ReadInput(os.Args[1])
	utils.PrintIntGrid(grid)


	lowPoints := day09.FindLowPoints(grid)

	var basinLengths []int
	// Keep track of basins so that we can make sure each location is only in 1 basin
	var basins []map[day09.Coord]int
	// For each low point, do a BFS to find what other points are included in its basin
	for _, lowPoint := range lowPoints {
		basin := day09.BfsBasin(grid, lowPoint, map[day09.Coord]int{}, basins)
		fmt.Printf("lowPoint: %v, has %v basin: %v\n",lowPoint, len(basin), basin)
		basins = append(basins, basin)
		basinLengths = append(basinLengths, len(basin))
	}
	// Find the biggest 3 basins
	sort.Ints(basinLengths)
	fmt.Printf("%v\n", basinLengths)


	// Multiply the last 3 sizes
	basinLengths = basinLengths[len(basinLengths)-3:]
	fmt.Printf("%v\n", basinLengths)
	result := 1
	for _, size := range basinLengths {
		result *= size
	}

	// 681210 too low

	fmt.Printf("Result: %v\n", result)
}
