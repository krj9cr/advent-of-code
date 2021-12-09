package day09

import (
	"bufio"
	"os"
)

func ReadInput(path string) [][]int {
	file, err := os.Open(path)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	if scanner.Err() != nil {
		panic(scanner.Err())
	}

	var grid [][]int
	for _, line := range lines {
		var gridRow []int
		for _, char := range line {
			intval := int(char - '0')
			gridRow = append(gridRow, intval)
		}
		grid = append(grid, gridRow)
	}

	return grid
}
