package day09

import (
	"bufio"
	"fmt"
	"os"
)

type Coord struct {
	I int
	J int
}

func BfsBasin(grid [][]int, curr Coord, basin map[Coord]int, basins []map[Coord]int) map[Coord]int {
	currVal := grid[curr.J][curr.I]
	// 9s aren't part of basins, so we can stop
	if currVal == 9 {
		return basin
	}

	// Check if the current location is already in another basin, if so, stop
	for _, b := range basins {
		//fmt.Printf("Checking other basins: %v\n", basins)
		if _, ok := b[curr]; ok {
			fmt.Printf("Found %v in another basin\n",curr)
			return basin
		}
	}

	// Otherwise, add the current location to this basin
	//fmt.Printf("Adding current location %v to basin %v\n", curr, basin)
	basin[curr] = 0
	fmt.Printf("Current val: %v at (%v, %v)\n", currVal, curr.I, curr.J)
	neighbors := GetNeighbors(grid, curr.I, curr.J)

	// Check each neighbor
	for _, neighbor := range neighbors {
		neighborVal := grid[neighbor.J][neighbor.I]
		fmt.Printf("  Checking neighbor val: %v\n", neighborVal)
		// 9s aren't part of basins, so we can continue
		if neighborVal == 9 {
			continue
		}

		// If allow flow
		if neighborVal > currVal {

			// Check if the neighbor location is already in another basin, if so, stop
			found := false
			for _, b := range basins {
				//fmt.Printf("Checking other basins: %v\n", basins)
				if _, ok := b[neighbor]; ok {
					fmt.Printf("Found %v in another basin\n",neighbor)
					found = true
				}
			}
			if !found {
				// Recurse
				basin[neighbor] = 0
				fmt.Printf("  Recursing with basin %v\n",basin)
				basin = BfsBasin(grid, neighbor, basin, basins)
			}
		}
	}
	return basin
}

// Returns list of neighbor values (not coords)
func GetNeighbors(grid [][]int, i int, j int) []Coord {
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

func FindLowPoints(grid [][]int) []Coord {
	var lowPoints []Coord
	for j, row := range grid {
		for i, item := range row {
			isLowPoint := true
			neighbors := GetNeighbors(grid, i, j)
			// fmt.Printf("Item: %v at (%v,%v)\n has neighbors: %v\n", item, i, j, neighbors)
			for _, n := range neighbors {
				if grid[n.J][n.I] <= item {
					isLowPoint = false
					break
				}
			}
			if isLowPoint {
				//fmt.Printf("Item: %v at (%v,%v) is low with neighbors: %v\n", item, i, j, neighbors)
				lowPoints = append(lowPoints, Coord{i,j})
			}
		}
	}
	return lowPoints
}

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
