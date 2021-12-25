package main

import (
	"fmt"
	"os"
	day24 "year_2021/day_24"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	lines := day24.ReadInput(os.Args[1])
	fmt.Printf("Input: %v\n", lines)

	input := 10
	variables := map[string]int{"w": 0, "x": 0, "y": 0, "z": 0}

	for _, line := range lines {
		day24.ProcessLine(line, variables, &input)
	}

	fmt.Printf("end: %v\n", variables)

	// fmt.Printf("Result: %v\n", result)
}
