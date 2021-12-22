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

	cubeRegion := day22.Cube{
		Xmin: -50, Xmax: 50,
		Ymin: -50, Ymax: 50,
		Zmin: -50, Zmax: 50,
		On: false,
	}

	var onAreas []day22.Cube

	// For each input cube
	for _, cube := range cubes {
		// If in cube region
		if cubeRegion.FullyContains(cube) {
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
	}
	numOn := 0
	fmt.Printf("On areas: %v\n", onAreas)
	for _, area := range onAreas {
		numOn += area.Volume()
	}

	fmt.Printf("Result: %v\n", numOn)
}
