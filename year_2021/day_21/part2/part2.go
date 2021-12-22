package main

import (
	"fmt"
	"os"
	day21 "year_2021/day_21"
)

const winningScore = 21
const boardSize = 10

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	p1, p2 := day21.ReadInput(os.Args[1])
	fmt.Printf("Player1 start: %v, Player2 start: %v\n", p1, p2)

	p1Wins, p2Wins := play(State{p1: p1, p2: p2, p1Score: 0, p2Score: 0, p1Turn: true})

	fmt.Printf("p1Wins: %v\np2Wins: %v\n", p1Wins, p2Wins)

	if p1Wins > p2Wins {
		fmt.Printf("P1 WINNER: %v\n", p1Wins)
	} else {
		fmt.Printf("P2 WINNER: %v\n", p2Wins)
	}
}

type State struct {
	p1, p2           int
	p1Score, p2Score int
	p1Turn           bool
}

type Wins struct {
	r1, r2 int
}

var possibleDiceRolls = map[int]int{3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}

var cache map[State]Wins = make(map[State]Wins)

// Return state or num wins?
func play(state State) (int, int) {
	// Base cases
	if state.p1Score >= winningScore {
		return 1, 0
	}
	if state.p2Score >= winningScore {
		return 0, 1
	}
	// Check cache to end early
	if wins, ok := cache[state]; ok {
		return wins.r1, wins.r2
	}
	p1Wins := 0
	p2Wins := 0
	for diceSum, occurrence := range possibleDiceRolls {
		nextState := state
		// Move whoever's turn it is
		if state.p1Turn {
			nextState.p1 += diceSum
			nextState.p1 %= boardSize
			if nextState.p1 == 0 {
				nextState.p1 = boardSize
			}
			nextState.p1Score += nextState.p1
			nextState.p1Turn = false
		} else {
			nextState.p2 += diceSum
			nextState.p2 %= boardSize
			if nextState.p2 == 0 {
				nextState.p2 = boardSize
			}
			nextState.p2Score += nextState.p2
			nextState.p1Turn = true
		}
		// Recurse, and multiply by the number of occurrences
		r1, r2 := play(nextState)
		p1Wins = p1Wins + (r1 * occurrence)
		p2Wins = p2Wins + (r2 * occurrence)
		fmt.Printf("Played: %v, p1Wins: %v, p2Wins: %v\n", state, p1Wins, p2Wins)
	}
	cache[state] = Wins{p1Wins, p2Wins}
	return p1Wins, p2Wins
}
