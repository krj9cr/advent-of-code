package main

import (
	"fmt"
	"os"
	day22 "year_2021/day_22"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	cubes := day22.ReadInput(os.Args[1])

	var onAreas []day22.Cube

	// For each input cube
	for _, cube := range cubes {
		// For each previous ON cube
		for j := range onAreas {
			c2 := onAreas[j]
			// if there's overlap, don't double count the volume
			// or, the cube is off, so we remove volume
			onAreas[j] = c2.Combine(cube)
		}
		if cube.On {
			onAreas = append(onAreas, cube)
		}
	}
	numOn := 0
	fmt.Printf("On areas: %v\n", onAreas)
	for _, area := range onAreas {
		numOn += area.Volume()
	}

	fmt.Printf("Result: %v\n", numOn)
}
