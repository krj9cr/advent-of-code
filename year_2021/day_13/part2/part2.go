package main

import (
	"fmt"
	"os"
	day13 "year_2021/day_13"
	"year_2021/utils"
)

// this is really part 1
func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	lines := day13.ReadInput(os.Args[1])
	fmt.Printf("Input: %v\n", lines)

	// Convert to map to remove duplicates
	currCoords := make(map[day13.Coord]bool)
	for _, coord := range lines.Coords {
		currCoords[coord] = true
	}
	// Print
	keys := make([]day13.Coord, len(currCoords))
	i := 0
	for k := range currCoords {
		keys[i] = k
		i++
	}
	utils.PrintStringGrid(day13.PlotDots(keys), "")

	// For THE FIRST fold
	fold := lines.Folds[0]
	newCoords := make(map[day13.Coord]bool)
	// For each point
	for coord, _ := range currCoords {
		// Reflect the point over the line
		newCoords[day13.Reflect(coord, fold)] = true
	}
	currCoords = newCoords
	fmt.Printf("currCoords: %v\n", currCoords)
	// Print grid
	keys = make([]day13.Coord, len(currCoords))
	i = 0
	for k := range currCoords {
		keys[i] = k
		i++
	}
	utils.PrintStringGrid(day13.PlotDots(keys), "")
	fmt.Printf("Visible dots: %v\n", len(currCoords))

	// Part 2
	// HKUJGAJZ lmao
	// Count remaining points
	fmt.Printf("Result: %v\n", len(currCoords))
}
