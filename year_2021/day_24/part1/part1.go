package main

import (
	"fmt"
	"os"
	day24 "year_2021/day_24"
)

/**
input[4] == input[3] - 1
input[5] == input[2] - 5
input[8] == input[7] + 3
input[9] == input[6] + 7
input[11] == input[10] + 2
input[12] == input[1] - 2
input[13] == input[0] + 4
**/
func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	lines := day24.ReadInput(os.Args[1])
	// fmt.Printf("Input: %v\n", lines)

	// Solved manually using the formulas above
	input := 59998426997979
	maxi := 0
	steps := 0
	for {
		inputNum := input
		fmt.Printf("trying: %v\n", input)
		variables := day24.ProcessLines(lines, day24.NumToInput(input))
		fmt.Printf("end: %v\n", variables)
		if variables["z"] == 0 {
			if inputNum > maxi {
				maxi = inputNum
				fmt.Printf("max: %v\n", maxi)
				break // for now, stop
			}
		}
		input -= 1
		steps += 1
	}
}
