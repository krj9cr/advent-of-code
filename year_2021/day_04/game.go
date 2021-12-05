package day04

import (
	"fmt"
)

type BingoGame struct {
	DrawNumbers []int
	Boards      []BingoBoard
}

func (game BingoGame) PlayGame() {
	// For each drawn number, play a round
	for round, drawnNumber := range game.DrawNumbers {
		fmt.Printf("Round %v, Drawing: %v\n", round, drawnNumber)
		done, answer, _ := game.PlayRound(drawnNumber)
		// If done, print answer, otherwise continue game
		if done {
			fmt.Printf("Result: %v\n", answer)
			return
		}
		game.PrintGame()
	}
	fmt.Println("NO WINNER")
}

// Returns (if done or not, answer, winner indexes)
func (game BingoGame) PlayRound(drawnNumber int) (bool, int, []int) {
	anyWinner := false
	result := 0
	var boardIndex []int
	// For each board, check drawn number and mark it
	for i := range game.Boards {
		board := game.Boards[i]
		board.CheckDrawnNumber(drawnNumber)
	}
	// For each board, check if winner
	for i, board := range game.Boards {
		// Check if this board is now a winning board
		winner, answer := board.IsWinner()
		if winner {
			result = answer * drawnNumber
			fmt.Printf("Sum: %v, Drawn number: %v, Result: %v\n", answer, drawnNumber, result)
			boardIndex = append(boardIndex, i)
			anyWinner = true
		}
	}
	// No winners yet
	return anyWinner, result, boardIndex
}

func (game BingoGame) RemoveBoards(boardsIndexes []int) []BingoBoard {
	var boards []BingoBoard
	for i, board := range game.Boards {
		found := false
		for _, index := range boardsIndexes {
			if i == index {
				found = true
				break
			}
		}
		if !found {
			boards = append(boards, board)
		}
	}
	return boards
}

func (game BingoGame) PlayForLastWinner() {
	// initialNumBoards := len(game.Boards)
	// For each drawn number, play a round
	for round, drawnNumber := range game.DrawNumbers {
		fmt.Printf("Round %v, Drawing: %v\n", round, drawnNumber)
		winner, answer, boardIndexes := game.PlayRound(drawnNumber)
		// If done, check win conditions, otherwise continue game
		if winner && len(game.Boards) == 1 {
			// If done, print answer, otherwise continue game
			fmt.Printf("Result: %v\n", answer)
			return
		} else if len(boardIndexes) > 0 {
			fmt.Printf("Removing boards %v\n", boardIndexes)
			game.Boards = game.RemoveBoards(boardIndexes)
		}
		game.PrintGame()
	}
	fmt.Println("NO WINNER")
}

func (game BingoGame) PrintGame() {
	fmt.Print("Draw numbers: ")
	for _, n := range game.DrawNumbers {
		fmt.Printf("%v, ", n)
	}
	fmt.Print("\n")

	for _, board := range game.Boards {
		board.PrintBoard()
	}
}
