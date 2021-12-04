package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	day03 "year_2021/day_03"
	"year_2021/utils"
)

func getRating(binaryLines [][]int, mostCommon bool) int64 {
	fmt.Printf("in get rating\n")
	day03.PrintBinaryLines(binaryLines)
	cols := len(binaryLines[0])
	for i := 0; i < cols; i++ {
		fmt.Printf("i: %v\n", i)
		if len(binaryLines) <= 1 {
			return day03.BinaryIntArrToInt64(binaryLines[0])
		}
		commonBit := day03.CommonBit(binaryLines, mostCommon, i)
		fmt.Printf("Common bit: %v\n", commonBit)
		binaryLines = day03.Keep(binaryLines, int(commonBit), i)
		fmt.Printf("Keep:\n")
		day03.PrintBinaryLines(binaryLines)
		fmt.Print("\n")
	}
	return day03.BinaryIntArrToInt64(binaryLines[0])
}

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
	fmt.Print("Binary lines: \n")
	day03.PrintBinaryLines(binaryLines)
	fmt.Print("\n")

	// var oxygenLines [][]int
	// copy(oxygenLines, binaryLines)
	oxygen := getRating(binaryLines, true)
	co2 := getRating(binaryLines, false)

	fmt.Printf("\nOxygen: %v, CO2: %v, Result: %v\n", oxygen, co2, oxygen*co2)
}
