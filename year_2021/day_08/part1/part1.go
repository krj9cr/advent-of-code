package main

import (
	"fmt"
	"os"
	day08 "year_2021/day_08"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	inputRows := day08.ReadInput(os.Args[1])
	// fmt.Printf("Input: %v\n", inputRows)

	// DO STUFF
	count := 0
	for _, row := range inputRows {
		for _, entry := range row.OutputValues {
			numDigits := len(entry)
			if numDigits == 2 || numDigits == 3 || numDigits == 4 || numDigits == 7 {
				count += 1
			}
		}
	}

	fmt.Printf("Result: %v\n", count)
}
