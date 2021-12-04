package day03

import (
	"fmt"
	"log"
	"strconv"
	"strings"
)

func PrintBinaryLines(binaryLines [][]int) {
	for _, line := range binaryLines {
		for _, num := range line {
			fmt.Printf("%v", num)
		}
		fmt.Print("\n")
	}
}

func BinaryIntArrToInt64(binary []int) int64 {

	stringResult := strings.Trim(strings.Join(strings.Fields(fmt.Sprint(binary)), ""), "[]")
	//fmt.Printf("String result: %v", stringResult)

	result, err := strconv.ParseInt(stringResult, 2, 64)
	if err != nil {
		panic(err)
	}
	return result
}

func CommonBit(binaryLines [][]int, mostCommon bool, i int) int {
	var numZero = 0
	var numOnes = 0
	for _, binaryRow := range binaryLines {
		if binaryRow[i] == 0 {
			numZero += 1
		} else if binaryRow[i] == 1 {
			numOnes += 1
		} else {
			log.Panicf("Unknown binary number? %v", binaryRow[i])
		}
	}
	var result = 1
	if mostCommon {
		result = 1
		if numOnes < numZero {
			result = 0
		}
	} else {
		result = 0
		if numOnes < numZero {
			result = 1
		}
	}
	return result
}

func GetCommonBitBinaryNum(binaryLines [][]int, mostCommon bool) int64 {
	cols := len(binaryLines[0])
	var binaryResult = make([]int, cols)
	for i := 0; i < cols; i++ {
		var numZero = 0
		var numOnes = 0
		for _, binaryRow := range binaryLines {
			if binaryRow[i] == 0 {
				numZero += 1
			} else if binaryRow[i] == 1 {
				numOnes += 1
			} else {
				log.Panicf("Unknown binary number? %v", binaryRow[i])
			}
		}
		var result = 1
		if mostCommon {
			if numOnes < numZero {
				result = 0
			}
		} else {
			if numOnes > numZero {
				result = 0
			}
		}
		binaryResult[i] = result
	}

	return BinaryIntArrToInt64(binaryResult)
}

func Keep(binaryLines [][]int, bit int, col int) [][]int {
	var result [][]int
	for _, binary := range binaryLines {
		if binary[col] == bit {
			result = append(result, binary)
		}
	}
	return result
}
