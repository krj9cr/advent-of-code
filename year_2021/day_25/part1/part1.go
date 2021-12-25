package main

import (
	"fmt"
	"os"
	day25 "year_2021/day_25"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	grid, east, south := day25.ReadInput(os.Args[1])
	// day25.PrintByteGrid(grid)
	// fmt.Printf("East: %v\n", east)
	// fmt.Printf("South: %v\n", south)

	// count steps until we done
	step := 1
	for {
		numChanged := 0
		// move east
		e, changed1 := day25.MoveHerd(grid, east, true)
		east = e
		grid = day25.GridFromHerds(len(grid[0]), len(grid), east, south)

		// move south
		s, changed2 := day25.MoveHerd(grid, south, false)
		south = s

		// Check if any have changed/moved, if so, stop
		numChanged += changed1 + changed2
		if numChanged == 0 {
			fmt.Printf("Total steps: %v\n", step)
			break
		}

		// make new grid
		grid = day25.GridFromHerds(len(grid[0]), len(grid), east, south)

		// fmt.Printf("After step: %v\n", step)
		// day25.PrintByteGrid(grid)
		// fmt.Printf("East: %v\n", east)
		// fmt.Printf("South: %v\n", south)
		step += 1
	}
}
