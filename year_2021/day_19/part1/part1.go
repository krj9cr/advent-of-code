package main

import (
	"fmt"
	"os"
	day19 "year_2021/day_19"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	scanners := day19.ReadInput(os.Args[1])
	// fmt.Printf("Input: %v\n", scanners)

	overlap := day19.FindOverlappingBeacons(0, 1, scanners)
	fmt.Printf("overlap 0,1: %v", overlap)

	// fmt.Printf("Result: %v\n", result)
}
