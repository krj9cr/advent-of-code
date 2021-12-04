package main

import (
	"fmt"
	"os"
	day04 "year_2021/day_04"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}

	// Read input into structs
	game := day04.ReadInput(os.Args[1])
	game.PrintGame()

	game.PlayGame()
}
