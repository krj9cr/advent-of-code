package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	day03 "year_2021/day_03"
	"year_2021/utils"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	lines, err := utils.ReadLinesToStrings(os.Args[1])
	if err != nil {
		log.Fatalf("readLines: %s", err)
	}
	utils.PrintStringSlice(lines)

	var binaryLines [][]int
	for _, l := range lines {
		var introw []int
		for _, c := range l {
			intval, err := strconv.Atoi(string(c))
			if err != nil {
				panic(err)
			}
			introw = append(introw, intval)
		}
		binaryLines = append(binaryLines, introw)
	}

	gamma := day03.GetCommonBitBinaryNum(binaryLines, true)
	epsilon := day03.GetCommonBitBinaryNum(binaryLines, false)

	fmt.Printf("\nGamma: %v, Epsilon: %v, Result: %v\n", gamma, epsilon, gamma*epsilon)
}
