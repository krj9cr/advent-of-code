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
	// fmt.Printf("Input: %v\n", lines)

	input := 99999999999999
	maxi := 0
	for {
		// input := day24.RandomInput()
		// fmt.Printf("trying input: %v\n", input)
		variables := day24.ProcessLines(lines, day24.NumToInput(input))
		// fmt.Printf("end: %v\n", variables)
		if variables["z"] == 0 {
			// modelNumber := day24.InputToNum(input)
			// fmt.Printf("Valid input: %v\n", modelNumber)
			if input > maxi {
				maxi = input
				fmt.Printf("max: %v\n", maxi)
			}
		}
		input -= 1
	}

	// fmt.Printf("Result: %v\n", result)
}
