package utils

import "fmt"

type Coord struct {
	I int
	J int
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

func PrintStringGrid(slice [][]string, splitter string) {
	for _, row := range slice {
		for _, item := range row {
			fmt.Printf("%v%v", item, splitter)
		}
		fmt.Print("\n")
	}
	fmt.Print("\n")
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

// Returns list of neighbor values (not coords)
func StringGetCardinalNeighbors(grid [][]string, i int, j int) []Coord {
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
func StringGetAllNeighbors(grid [][]string, i int, j int) []Coord {
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
