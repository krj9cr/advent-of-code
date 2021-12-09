package main

import (
	"fmt"
	"os"
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

	sum := 0
	lowPoints := day09.FindLowPoints(grid)
	for _, point := range lowPoints {
		sum += grid[point.J][point.I] + 1
	}

	fmt.Printf("Result: %v\n", sum)
}
