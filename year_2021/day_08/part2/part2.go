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
	sum := 0
	for _, row := range inputRows {

		entryMap := make(map[string]int)
		var fivers []string
		var sixers []string
		for _, entry := range row.SignalPatterns {
			numDigits := len(entry)
			if numDigits == 2 {
				entryMap[entry] = 1
			} else if numDigits == 3 {
				entryMap[entry] = 7
			} else if numDigits == 4 {
				entryMap[entry] = 4
			} else if numDigits == 7 {
				entryMap[entry] = 8
			} else if numDigits == 5 { // 2, 3, or 5
				fivers = append(fivers, entry)
			} else if numDigits == 6 { // 0, 6, or 9
				sixers = append(sixers, entry)
			}
		}
		// TODO: map fivers and sixers to entryMap

		// For each outputValue, check if it has the same letters contained
		// as one of the keys in entryMap to determine its number
		// for _, entry := range row.OutputValues {

		// }
	}

	fmt.Printf("Result: %v\n", sum)
}
