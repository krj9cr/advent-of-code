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
	utils.PrintIntSlice(lines)

	var sums []int
	var size = len(lines)
	for i, l := range lines {
		if i+2 < size {
			var next1 = lines[i+1]
			var next2 = lines[i+2]
			var sum = l + next1 + next2
			sums = append(sums, sum)
		}
	}

	fmt.Printf("SUMS:\n")
	utils.PrintIntSlice(sums)
	var count int = day01.CountIncreasing(sums)
	fmt.Printf("Count: %v\n", count)
}
