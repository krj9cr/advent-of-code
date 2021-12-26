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

	input := 59998426997979
	// tried := make(map[int]bool)
	maxi := 0
	steps := 0
	for {
		// input := day24.RandomInput()
		inputNum := input //day24.InputToNum(input)
		// if _, ok := tried[inputNum]; ok {
		// 	continue
		// }
		// tried[inputNum] = true
		fmt.Printf("trying: %v\n", input)
		variables := day24.ProcessLines(lines, day24.NumToInput(input))
		fmt.Printf("end: %v\n", variables)
		if variables["z"] == 0 {
			// fmt.Printf("Valid input: %v\n", modelNumber)
			if inputNum > maxi {
				maxi = inputNum
				fmt.Printf("max: %v\n", maxi)
				break // for now, stop
			}
		}
		// if steps > 1 {
		// 	break
		// }
		input -= 1
		steps += 1
	}
}
