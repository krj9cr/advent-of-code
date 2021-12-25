package day25

import (
	"bufio"
	"fmt"
	"os"
	"year_2021/utils"
)

func PrintByteGrid(grid [][]byte) {
	for _, row := range grid {
		for _, item := range row {
			fmt.Printf("%v", string(item))
		}
		fmt.Print("\n")
	}
	fmt.Print("\n")
}

func MoveHerd(grid [][]byte, herd []utils.Coord, east bool) ([]utils.Coord, int) {
	numChanged := 0
	var newHerd []utils.Coord
	for _, cuc := range herd {
		moved := MoveCuc(grid, cuc, east)
		if moved == nil {
			newHerd = append(newHerd, cuc)
		} else {
			newHerd = append(newHerd, *moved)
			numChanged += 1
		}
	}
	return newHerd, numChanged
}

func MoveCuc(grid [][]byte, cuc utils.Coord, east bool) *utils.Coord {
	newI := cuc.I
	newJ := cuc.J
	if east {
		newI = (cuc.I + 1) % len(grid[0]) // wrap
	} else {
		newJ = (cuc.J + 1) % len(grid)
	}
	if string(grid[newJ][newI]) == "." {
		return &utils.Coord{I: newI, J: newJ}
	}
	return nil
}

func GridFromHerds(w int, h int, east []utils.Coord, south []utils.Coord) [][]byte {
	var grid [][]byte
	for j := 0; j < h; j++ {
		var row []byte
		for i := 0; i < w; i++ {
			row = append(row, '.')
		}
		// row := make([]byte, w, '.')
		grid = append(grid, row)
	}
	for _, cuc := range east {
		grid[cuc.J][cuc.I] = '>'
	}
	for _, cuc := range south {
		grid[cuc.J][cuc.I] = 'v'
	}
	return grid
}

func ReadInput(path string) ([][]byte, []utils.Coord, []utils.Coord) {
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

	var grid [][]byte
	var east []utils.Coord
	var south []utils.Coord
	for j, line := range lines {
		for i, char := range line {
			if char == '>' {
				east = append(east, utils.Coord{I: i, J: j})
			} else if char == 'v' {
				south = append(south, utils.Coord{I: i, J: j})
			}
		}
		grid = append(grid, []byte(line))
	}

	return grid, east, south
}
