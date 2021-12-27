package main

import (
	"fmt"
	"log"
	"os"
	day02 "year_2021/day_02"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	lines, err := day02.ReadInput(os.Args[1])
	if err != nil {
		log.Fatalf("readLines: %s", err)
	}
	// day02.PrintCommands(lines)

	horizontal := 0
	vertical := 0
	for _, command := range lines {
		switch command.Direction {
		case "forward":
			horizontal += command.Amount
		case "down":
			vertical += command.Amount
		case "up":
			vertical -= command.Amount
		default:
			log.Panicf("Unknown direction: %v", command.Direction)
		}
	}

	fmt.Printf("horizontal: %v, vertical: %v, result: %v\n", horizontal, vertical, horizontal*vertical)
}
