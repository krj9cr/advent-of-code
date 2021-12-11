package day11

import (
	"bufio"
	"os"
	"year_2021/utils"
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

	var ints [][]int
	for _, line := range lines {
		var row []int
		for _, char := range line {
			row = append(row, int(char-'0'))
		}
		ints = append(ints, row)
	}

	return ints
}

func Flash(grid [][]int, i int, j int) int {
	numFlashes := 0
	if grid[j][i] > 9 {
		grid[j][i] = 0
		numFlashes += 1
		// Bump up neighbors, unless a neighbor is 0, already
		neighbors := utils.GetAllNeighbors(grid, i, j)
		for _, neighbor := range neighbors {
			if grid[neighbor.J][neighbor.I] > 0 {
				grid[neighbor.J][neighbor.I] += 1
			}
			// Check if it needs to flash, now
			if grid[neighbor.J][neighbor.I] > 9 {
				numFlashes += Flash(grid, neighbor.I, neighbor.J)
			}
		}
	}
	return numFlashes
}
