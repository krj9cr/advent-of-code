package main

import (
	"fmt"
	"os"
	day15 "year_2021/day_15"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	lines := day15.ReadInput(os.Args[1])
	fmt.Printf("Input: %v\n", lines)

	// DO STUFF

	// fmt.Printf("Result: %v\n", result)
}
