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
	for i := range game.Boards {
		board := game.Boards[i]
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

// func (game BingoGame) RemoveBoard(i int) []BingoBoard {
// 	game.Boards[i] = game.Boards[len(game.Boards)-1]
// 	return game.Boards[:len(game.Boards)-1]
// }

// func (game BingoGame) RemoveBoards(boardsIndexes []int) []BingoBoard {
// 	for i := 0; i < len(game.Boards); i++ {
// 		for _, boardIndex := range boardsIndexes {
// 			if i == boardIndex {
// 				game.Boards = append(game.Boards[:i], game.Boards[i+1:]...)
// 				//a = a[:i+copy(a[i:], a[i+1:])]
// 				i-- // Since we just deleted a[i], we must redo that index
// 			}
// 		}
// 	}
// }

func (game BingoGame) PlayForLastWinner() {
	initialNumBoards := len(game.Boards)
	// For each drawn number, play a round
	for round, drawnNumber := range game.DrawNumbers {
		fmt.Printf("Round %v, Drawing: %v\n", round, drawnNumber)
		winner, answer, boardIndexes := game.PlayRound(drawnNumber)
		// If done, check win conditions, otherwise continue game
		if winner {
			if len(game.Boards) == 1 {
				// If done, print answer, otherwise continue game
				fmt.Printf("Result: %v\n", answer)
				return
			}
			fmt.Printf("Board indexes: %v\n", boardIndexes)
			// check if there's one last board
			if len(boardIndexes) == initialNumBoards-1 {
				// Find the board that's last
				lastIndex := 0
				for i := range game.Boards {
					found := false
					for _, b := range boardIndexes {
						if i == b {
							found = true
							break
						}
					}
					if !found {
						lastIndex = i
						break
					}
				}
				fmt.Printf("LAST BOARD: %v\n", lastIndex)
				// Remove all the boards
				game.Boards = []BingoBoard{game.Boards[lastIndex]}
				// Play until it wins
				game.PrintGame()
			}
			// remove board and conintue
			// fmt.Printf("Removing boards %v\n", boardIndexes)
			// for i, boardIndex := range boardIndexes {
			// 	game.Boards = game.RemoveBoard(boardIndex - i)
			// }
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
