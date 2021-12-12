package main

import (
	"fmt"
	"os"
	day13 "year_2021/day_13"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	lines := day13.ReadInput(os.Args[1])
	fmt.Printf("Input: %v\n", lines)

	// DO STUFF

	// fmt.Printf("Result: %v\n", result)
}
