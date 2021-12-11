package utils

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

// readLines reads a whole file into memory
// and returns a slice of its lines.
func ReadLinesToStrings(path string) ([]string, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	return lines, scanner.Err()
}

func ReadLinesToInts(path string) ([]int, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	var ints []int
	for _, l := range lines {
		var intval, err = strconv.Atoi(l)
		if err != nil {
			panic(err)
		}
		ints = append(ints, intval)
	}
	return ints, scanner.Err()
}

func PrintStringSlice(slice []string) {
	for _, s := range slice {
		fmt.Printf("%v\n", s)
	}
}

func PrintIntSlice(slice []int) {
	for _, s := range slice {
		fmt.Printf("%d\n", s)
	}
}

func PrintIntGrid(slice [][]int) {
	for _, row := range slice {
		for _, item := range row {
			fmt.Printf("%v ", item)
		}
		fmt.Print("\n")
	}
	fmt.Print("\n")
}

func PrintStringGrid(slice [][]string) {
	for _, row := range slice {
		for _, item := range row {
			fmt.Printf("%v ", item)
		}
		fmt.Print("\n")
	}
	fmt.Print("\n")
}

type Coord struct {
	I int
	J int
}

// Returns list of neighbor values (not coords)
func GetCardinalNeighbors(grid [][]int, i int, j int) []Coord {
	up := j - 1
	down := j + 1
	left := i - 1
	right := i + 1
	height := len(grid)
	width := len(grid[0])

	var neighbors []Coord
	if up >= 0 {
		neighbors = append(neighbors, Coord{i, up})
	}
	if left >= 0 {
		neighbors = append(neighbors, Coord{left, j})
	}
	if down < height {
		neighbors = append(neighbors, Coord{i, down})
	}
	if right < width {
		neighbors = append(neighbors, Coord{right, j})
	}
	return neighbors
}

// Returns list of neighbor coordinates, including diagonals
func GetAllNeighbors(grid [][]int, i int, j int) []Coord {
	up := j - 1
	down := j + 1
	left := i - 1
	right := i + 1
	height := len(grid)
	width := len(grid[0])

	var neighbors []Coord
	if up >= 0 {
		neighbors = append(neighbors, Coord{i, up})
		if left >= 0 {
			neighbors = append(neighbors, Coord{left, up})
		}
		if right < width {
			neighbors = append(neighbors, Coord{right, up})
		}
	}
	if left >= 0 {
		neighbors = append(neighbors, Coord{left, j})
	}
	if down < height {
		neighbors = append(neighbors, Coord{i, down})
		if left >= 0 {
			neighbors = append(neighbors, Coord{left, down})
		}
		if right < width {
			neighbors = append(neighbors, Coord{right, down})
		}
	}
	if right < width {
		neighbors = append(neighbors, Coord{right, j})
	}
	return neighbors
}
