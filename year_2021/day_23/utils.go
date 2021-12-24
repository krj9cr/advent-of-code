package day23

import (
	"bufio"
	"os"
	"year_2021/utils"
)

type Room int

const (
	ARoom   Room = 0
	BRoom   Room = 1
	CRoom   Room = 2
	DRoom   Room = 3
	Hallway Room = 4
	Doorway Room = 5
	Wall    Room = 6
)

type AmphipodType string

const (
	A AmphipodType = "A"
	B AmphipodType = "B"
	C AmphipodType = "C"
	D AmphipodType = "D"
)

type Amphipod struct {
	Moving   bool
	Atype    AmphipodType
	Location utils.Coord
}

type Board struct {
	Spaces    map[utils.Coord]Room
	Amphipods []Amphipod
}

func ReadInput(path string) []string {
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

	// parse into structs
	var grid [][]Room
	var amphs []Amphipod
	for j, line := range lines {
		var row []Room
		for i, char := range line {
			room := Wall
			if char == '.' {
				if i == 3 || i == 5 || i == 7 || i == 9 {
					room = Doorway
				} else {
					room = Hallway
				}
			} else {
				// it's a letter in a room
				// save the room
				if j == 2 || j == 3 {
					if i == 3 {
						room = ARoom
					} else if i == 5 {
						room = BRoom
					} else if i == 7 {
						room = CRoom
					} else if i == 9 {
						room = DRoom
					}
				}
				// save the letter
				a := Amphipod{Atype: A}
				if char == 'B' {
					a.Atype = B
				} else if char == 'C' {
					a.Atype = C
				} else if char == 'D' {
					a.Atype = D
				}
			} // else, it's a wall
			row = append(row, room)
		}
		grid = append(grid, row)
	}

	return lines
}
