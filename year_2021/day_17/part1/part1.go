package main

import (
	"fmt"
	"os"
	day17 "year_2021/day_17"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	targetArea := day17.ReadInput(os.Args[1])
	fmt.Printf("Input: %v\n", targetArea)

	velXMax := 1000
	velYMax := 1000
	maxHeight := 0
	var maxVel day17.Velocity
	// For velocities within some range...
	for x := 0; x < velXMax; x++ {
		for y := 0; y < velYMax; y++ {
			// Run simulations
			velocity := day17.Velocity{X: x, Y: y}
			fmt.Printf("Trying velocity: %v\n", velocity)
			intersects, mHeight := day17.RunSim(targetArea, velocity)
			if intersects && mHeight > maxHeight {
				maxHeight = mHeight
				maxVel = velocity
			}
		}
	}
	// Get max height
	fmt.Printf("Max height: %v with velocity: %v\n", maxHeight, maxVel)
}
