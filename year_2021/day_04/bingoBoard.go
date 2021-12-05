package day04

import (
	"fmt"

	"github.com/fatih/color"
)

type BingoTile struct {
	Value  int
	Marked bool
}

type BingoBoard struct {
	Board [][]BingoTile
}

// Prints the board with colors for the marked tiles
func (board BingoBoard) PrintBoard() {
	d := color.New(color.FgCyan, color.Bold)
	for _, row := range board.Board {
		for _, tile := range row {
			if tile.Marked {
				if tile.Value < 10 {
					d.Printf(" %v ", tile.Value)
				} else {
					d.Printf("%v ", tile.Value)
				}
			} else {
				if tile.Value < 10 {
					fmt.Printf(" %v ", tile.Value)
				} else {
					fmt.Printf("%v ", tile.Value)
				}
			}
		}
		fmt.Print("\n")
	}
	fmt.Print("\n")
}

// Should modify the board in place, hopefully
func (board BingoBoard) CheckDrawnNumber(drawnNumber int) {
	for i := range board.Board {
		for j := range board.Board[i] {
			if board.Board[i][j].Value == drawnNumber {
				board.Board[i][j].Marked = true
			}
		}
	}
}

func (board BingoBoard) SumUnmarked() int {
	fmt.Print("WINNER: \n")
	board.PrintBoard()
	sum := 0
	for _, row := range board.Board {
		for _, item := range row {
			if !item.Marked {
				sum += item.Value
			}
		}
	}
	return sum
}

// Returns (if winner or not, sum of winning numbers)
func (board BingoBoard) IsWinner() (bool, int) {
	h := len(board.Board)
	w := len(board.Board[0])

	winner := false
	// check each row
	for _, row := range board.Board {
		// assume row is a winner until proven otherwise
		winner = true
		for _, item := range row {
			if !item.Marked {
				winner = false
				break
			}
		}
		if winner {
			return true, board.SumUnmarked()
		}
	}

	// check each col
	for j := 0; j < w; j++ {
		winner = true
		for i := 0; i < h; i++ {
			item := board.Board[i][j]
			if !item.Marked {
				winner = false
				break
			}
		}
		if winner {
			return true, board.SumUnmarked()
		}
	}

	// DIRECTIONS SAY DIAGONALS DON'T COUNT!!!

	if winner {
		return true, board.SumUnmarked()
	}

	return false, 0
}
