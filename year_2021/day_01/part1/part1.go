package main

import (
	"fmt"
	"log"
	"os"
	day01 "year_2021/day_01"
	"year_2021/utils"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	lines, err := utils.ReadLinesToInts(os.Args[1])
	if err != nil {
		log.Fatalf("readLines: %s", err)
	}
	// utils.PrintIntSlice(lines)

	var count int = day01.CountIncreasing(lines)
	fmt.Printf("Count: %v\n", count)
}
