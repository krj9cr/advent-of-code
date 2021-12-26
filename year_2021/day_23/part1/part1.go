package main

import (
	"fmt"
	"os"
	day23 "year_2021/day_23"
)

// Solved MANUALLY LOL
// This code currently has a stack overflow
func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	state := day23.ReadInput(os.Args[1])
	state.PrintRooms()
	day23.StateCosts[day23.FinalStateStr] = 16000

	day23.Step(state)

	fmt.Printf("Result: %v\n", day23.StateCosts[day23.FinalStateStr])
}
