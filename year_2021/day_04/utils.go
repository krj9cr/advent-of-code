package day04

import (
	"bufio"
	"os"
	"strconv"
	"strings"
)

func ReadInput(path string) BingoGame {
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

	var drawNumbers []int
	for _, n := range strings.Split(lines[0], ",") {
		intval, err := strconv.Atoi(n)
		if err != nil {
			panic(err)
		}
		drawNumbers = append(drawNumbers, intval)
	}

	var boards []BingoBoard
	var tiles [][]BingoTile = make([][]BingoTile, 0)
	// Start reading in boards from 2nd line
	for i := 2; i < len(lines); i++ {
		line := lines[i]
		// check if "empty" line
		if len(line) < 3 {
			// setup and clean out the tile
			boards = append(boards, BingoBoard{Board: tiles})
			tiles = make([][]BingoTile, 0)
		} else {
			var tileRow []BingoTile
			// Add row of ints to tile
			for _, n := range strings.Fields(line) {
				intval, err := strconv.Atoi(n)
				if err != nil {
					panic(err)
				}
				tileRow = append(tileRow, BingoTile{Value: intval, Marked: false})
			}
			tiles = append(tiles, tileRow)
		}
	}
	// add the last board
	boards = append(boards, BingoBoard{Board: tiles})

	return BingoGame{DrawNumbers: drawNumbers, Boards: boards}
}
