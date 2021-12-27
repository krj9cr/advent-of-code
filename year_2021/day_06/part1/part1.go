package main

import (
	"fmt"
	"os"
	day06 "year_2021/day_06"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	fish := day06.ReadInput(os.Args[1])
	// fmt.Printf("Input: %v\n", fish)

	numDays := 80
	spawnDays := 6
	initialDays := 8

	for day := 1; day <= numDays; day++ {
		for i := range fish {
			f := fish[i]
			// check if spawn
			if f == 0 {
				fish = append(fish, initialDays)
				fish[i] = spawnDays
			} else {
				fish[i] -= 1
			}
		}
		// fmt.Printf("After %v day: %v\n", day, fish)
	}

	fmt.Printf("Result: %v\n", len(fish))
}
