package main

import (
	"fmt"
	"os"
	day21 "year_2021/day_21"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	p1, p2 := day21.ReadInput(os.Args[1])
	fmt.Printf("Player1 start: %v, Player2 start: %v\n", p1, p2)

	boardSize := 10

	diceMax := 100
	diceCurr := 0
	dieRolls := 0

	winningScore := 1000
	p1Score := 0
	p2Score := 0

	// Play forever
	for {
		// Until a player is past a score (checked below)

		// Player 1 goes
		rollSum := 0
		var p1Rolls []int
		// Roll the dice 3 times
		for roll := 0; roll < 3; roll++ {
			diceCurr += 1
			p1Rolls = append(p1Rolls, diceCurr)
			rollSum += diceCurr

			dieRolls += 1
			if diceCurr >= diceMax {
				diceCurr = 0
			}
		}
		p1 += rollSum
		p1 %= boardSize
		if p1 == 0 {
			p1 = boardSize
		}
		p1Score += p1
		if p1Score >= winningScore {
			fmt.Printf("Player 1 wins with: %v\n", p1Score)
			fmt.Printf("Player 2 has: %v points, die was rolled: %v\n", p2Score, dieRolls)
			fmt.Printf("Result: %v\n", p2Score*dieRolls)
			break
		}

		// Player 2 goes
		rollSum = 0
		var p2Rolls []int
		// Roll the dice 3 times
		for roll := 0; roll < 3; roll++ {
			diceCurr += 1
			p2Rolls = append(p2Rolls, diceCurr)
			rollSum += diceCurr

			dieRolls += 1
			if diceCurr >= diceMax {
				diceCurr = 0
			}
		}
		p2 += rollSum
		p2 %= boardSize
		if p2 == 0 {
			p2 = boardSize
		}
		p2Score += p2
		if p2Score >= winningScore {
			fmt.Printf("Player 2 wins with: %v\n", p2Score)
			fmt.Printf("Player 1 has: %v points, die was rolled: %v\n", p1Score, dieRolls)
			fmt.Printf("Result: %v\n", p1Score*dieRolls)
			break
		}

		fmt.Printf("Player 1 rolls %v and moves to %v for a total score of %v\n", p1Rolls, p1, p1Score)
		fmt.Printf("Player 2 rolls %v and moves to %v for a total score of %v\n", p2Rolls, p2, p2Score)
	}
}
