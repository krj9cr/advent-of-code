package day13

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
)

type Coord struct {
	I int
	J int
}

type Fold struct {
	Dir string // either "x" or "y"
	Val int
}

type OrigamiInstructions struct {
	Coords []Coord
	Folds  []Fold
}

func ReflectAAcrossB(a int, b int) int {
	// Only reflect if we need to
	if a > b {
		dist := int(math.Abs(float64(a) - float64(b)))
		return b - dist
	} else {
		return a
	}
}

func Reflect(coord Coord, fold Fold) Coord {
	if fold.Dir == "x" {
		newI := ReflectAAcrossB(coord.I, fold.Val)
		return Coord{newI, coord.J}
	} else if fold.Dir == "y" {
		newJ := ReflectAAcrossB(coord.J, fold.Val)
		return Coord{coord.I, newJ}
	} else {
		log.Panicf("unknown fold dir: %v", fold.Dir)
		return Coord{}
	}
}

func PlotDots(coords []Coord) [][]string {
	maxx := 0
	maxy := 0
	for _, coord := range coords {
		if coord.I > maxx {
			maxx = coord.I
		}
		if coord.J > maxy {
			maxy = coord.J
		}
	}
	fmt.Printf("maxx: %v, maxy: %v\n", maxx, maxy)
	// init grid
	var grid [][]string
	for j := 0; j < maxy+1; j++ {
		var row []string
		for i := 0; i < maxx+1; i++ {
			row = append(row, ".")
		}
		grid = append(grid, row)
	}
	// utils.PrintStringGrid(grid, "")
	// Add coords
	for _, coord := range coords {
		grid[coord.J][coord.I] = "#"
	}
	return grid
}

func ReadInput(path string) OrigamiInstructions {
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

	// Top section
	topSection := true
	var coords []Coord
	var folds []Fold
	for _, line := range lines {
		// Hit the newline
		if len(line) <= 1 {
			topSection = false
			continue
		}
		if topSection {
			split := strings.Split(line, ",")
			if len(split) != 2 {
				log.Panicf("could not parse line: %v", line)
			}
			i, err := strconv.Atoi(split[0])
			if err != nil {
				log.Panicf("could not parse line: %v", line)
			}
			j, err := strconv.Atoi(split[1])
			if err != nil {
				log.Panicf("could not parse line: %v", line)
			}
			coords = append(coords, Coord{i, j})
		} else {
			split := strings.Split(line, " ")
			if len(split) != 3 {
				log.Panicf("could not parse line: %v", line)
			}
			split2 := strings.Split(split[2], "=")
			if len(split2) != 2 {
				log.Panicf("could not parse line: %v", line)
			}
			dir := split2[0]
			value, err := strconv.Atoi(split2[1])
			if err != nil {
				log.Panicf("could not parse line: %v", line)
			}
			folds = append(folds, Fold{dir, value})
		}
	}

	return OrigamiInstructions{coords, folds}
}
