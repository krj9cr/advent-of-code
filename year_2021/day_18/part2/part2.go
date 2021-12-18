package main

import (
	"fmt"
	"os"
	day18 "year_2021/day_18"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	trees := day18.ReadInput(os.Args[1])
	for _, tree := range trees {
		fmt.Printf("Tree: %v\n", tree)
	}

	// DO STUFF

	// fmt.Printf("Result: %v\n", result)
}
