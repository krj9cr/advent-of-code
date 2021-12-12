package main

import (
	"fmt"
	"os"
	day12 "year_2021/day_12"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	graph := day12.ReadInput(os.Args[1])
	fmt.Printf("GRAPH:\n%v\n", graph)

	numPaths := graph.CountPaths("start", "end")

	fmt.Printf("Result: %v\n", numPaths)
}
