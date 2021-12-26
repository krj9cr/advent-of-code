package day23

import (
	"bufio"
	"container/heap"
	"fmt"
	"log"
	"math"
	"os"
	"year_2021/utils"
)

type RoomType int

const (
	ARoom   RoomType = 0
	BRoom   RoomType = 1
	CRoom   RoomType = 2
	DRoom   RoomType = 3
	Hallway RoomType = 4
	Doorway RoomType = 5
)

type Room struct {
	Rtype RoomType
	Value string // one of A, B, C, D, or .
}

func (room Room) IsOccupied() bool {
	return room.Value == "A" || room.Value == "B" || room.Value == "C" || room.Value == "D"
}

func (state State) GetAdjacentOpenRooms(coord utils.Coord) []utils.Coord {
	var result []utils.Coord
	up := utils.Coord{I: coord.I, J: coord.J - 1}
	room2, ok := state.Rooms[up]
	if ok && room2.Value == "." {
		result = append(result, up)
	}
	down := utils.Coord{I: coord.I, J: coord.J + 1}
	room2, ok = state.Rooms[down]
	if ok && room2.Value == "." {
		result = append(result, down)
	}
	left := utils.Coord{I: coord.I - 1, J: coord.J}
	room2, ok = state.Rooms[left]
	if ok && room2.Value == "." {
		result = append(result, left)
	}
	right := utils.Coord{I: coord.I + 1, J: coord.J}
	room2, ok = state.Rooms[right]
	if ok && room2.Value == "." {
		result = append(result, right)
	}
	return result
}

func (state State) CanMove(coord utils.Coord) bool {
	room, ok := state.Rooms[coord]
	if ok && room.IsOccupied() {
		return len(state.GetAdjacentOpenRooms(coord)) > 0
	}
	return false
}

func (room Room) CostToMove() int {
	if room.Value == "A" {
		return 1
	} else if room.Value == "B" {
		return 10
	} else if room.Value == "C" {
		return 100
	} else if room.Value == "D" {
		return 1000
	}
	log.Panicf("trying to get cost to move for non-letter room: %v\n", room)
	return 0
}

type State struct {
	Rooms map[utils.Coord]Room
	Cost  int
}

// In the list of rooms, find the room that matches the coordinate
// func FindCoordRoom(coord utils.Coord, rooms []Room) *Room {
// 	for _, room := range rooms {
// 		if room.Coord == coord {
// 			return &room
// 		}
// 	}
// 	return nil
// }

// Return the open home rooms for a given letter (room)
func (state State) GetOpenLetterHomes(room Room) []utils.Coord {
	var result []utils.Coord
	for coord, r := range state.Rooms {
		if r.Rtype == ARoom && room.Value == "A" && r.Value == "." {
			result = append(result, coord)
		} else if r.Rtype == BRoom && room.Value == "B" && r.Value == "." {
			result = append(result, coord)
		} else if r.Rtype == CRoom && room.Value == "C" && r.Value == "." {
			result = append(result, coord)
		} else if r.Rtype == DRoom && room.Value == "D" && r.Value == "." {
			result = append(result, coord)
		}
	}
	return result
}

func (state State) GetOpenHallways() []utils.Coord {
	var result []utils.Coord
	for coord, room := range state.Rooms {
		if room.Rtype == Hallway && room.Value == "." {
			result = append(result, coord)
		}
	}
	return result
}

// Given a state (set of Rooms), and set of previous states and costs
// return the... next state and new set of previous states (including next state)
func Step(state State, previousStates map[string]int) (*State, map[string]int) {
	// Check if we're in a final state
	//   where we won, or there... are no more meaningful moves D:.. or the cost is too high?
	if state.Done() {
		return &state, previousStates
	}

	nextRooms := make(map[utils.Coord]Room)
	for key, val := range state.Rooms {
		nextRooms[key] = val
	}

	// For each room
	for coord, room := range state.Rooms {
		// if letter and can move
		if state.CanMove(coord) {
			// see if there's a path to its Room, prioritize that path
			openHomes := state.GetOpenLetterHomes(room)
			for _, home := range openHomes {
				homeRoom, ok := state.Rooms[home]
				if !ok {
					log.Panicf("could not find room: %v\n", home)
				}
				// Try a path, return that state if it works
				cost := Astar(state, coord, home)
				val, ok := cost[home]
				if ok { // there is a path
					// move the letter from coord to home
					emptyRoom := Room{Rtype: room.Rtype, Value: "."}
					nextRooms[coord] = emptyRoom
					letterRoom := Room{Rtype: homeRoom.Rtype, Value: room.Value}
					nextRooms[home] = letterRoom

					nextCost := state.Cost + val
					nextState := State{Rooms: nextRooms, Cost: nextCost}

					prevStateCost, ok := previousStates[nextState.RoomsToString()]
					if ok {
						if prevStateCost > nextCost {
							previousStates[nextState.RoomsToString()] = nextCost
						} else {
							nextState.Cost = prevStateCost
						}
					}
					return Step(nextState, previousStates)
				}
			}
			// else, try moving the letter to each of the Hallway spots, creating branching states
			for _, hallway := range state.GetOpenHallways() {
				hallwayRoom, ok := state.Rooms[hallway]
				if !ok {
					log.Panic("could not find room: %v\n", hallway)
				}
				cost := Astar(state, coord, hallway)
				val, ok := cost[hallway]
				if ok { // there is a path
					// move it
					// get new cost
					// Step...?
				}
			}
			// Save states and costs
			//   check if previous state had a lower cost, and use that if so
			// TODO: consider checking for exceedingly high cost
		} // else, this letter can't move
	}
	// we get here if no letters can move... unlikely
	return nil, previousStates
}

// guesses the cost of going from current position to goal
// should always underestimate the actual cost
func heuristic(goal utils.Coord, x2 int, y2 int) int {
	x1 := goal.I
	y1 := goal.J
	dist := math.Abs(float64(x1)-float64(x2)) + math.Abs(float64(y1)-float64(y2))
	return int(dist)
}

func Astar(state State, start utils.Coord, end utils.Coord) map[utils.Coord]int {
	// init
	pq := make(utils.PriorityQueue, 0)

	// came_from := map[utils.Coord]*utils.Coord{} // keeps track of our path to the goal
	cost_so_far := map[utils.Coord]int{} // keeps track of cost to arrive at ((x, y))

	// add start infos
	item := &utils.Item{
		Value:    start,
		Priority: 0,
	}
	heap.Push(&pq, item)
	// came_from[start] = nil
	cost_so_far[start] = 0

	// Init heap so that it sorts for us
	heap.Init(&pq)

	// while queue not empty
	for ok := true; ok; ok = pq.Len() > 0 {
		// fmt.Printf("Popped item: %v\n", item)
		item := heap.Pop(&pq).(*utils.Item)
		x := item.Value.I
		y := item.Value.J
		currCoord := item.Value

		if x == end.I && y == end.J {
			break
		}

		// for each adjacent open room
		room, ok := state.Rooms[currCoord]
		if !ok {
			log.Panicf("could not find room: %v\n", currCoord)
		}
		neighbors := state.GetAdjacentOpenRooms(currCoord)
		for _, neighbor := range neighbors {
			x2 := neighbor.I
			y2 := neighbor.J
			cost_to_move := room.CostToMove() // note this could vary on implementation
			new_cost := cost_so_far[currCoord] + cost_to_move
			next_spot := utils.Coord{I: x2, J: y2}
			_, found := cost_so_far[next_spot]
			// if next_spot in cost_so_far, and if it's cheap to move
			if !found || new_cost < cost_so_far[next_spot] {
				cost_so_far[next_spot] = new_cost
				priority := new_cost + heuristic(end, x2, y2)
				item := &utils.Item{
					Value:    next_spot,
					Priority: priority,
				}
				heap.Push(&pq, item)
			}
		}
	}
	return cost_so_far
}

func (state State) Done() bool {
	for _, room := range state.Rooms {
		if room.Rtype == ARoom && room.Value != "A" {
			return false
		}
		if room.Rtype == BRoom && room.Value != "B" {
			return false
		}
		if room.Rtype == CRoom && room.Value != "C" {
			return false
		}
		if room.Rtype == DRoom && room.Value != "D" {
			return false
		}
	}
	return true
}

func (state State) RoomsToString() string {
	grid := state.ToGrid()
	result := ""
	for _, row := range grid {
		for _, item := range row {
			result += fmt.Sprintf("%v", item)
		}
	}
	return result
}

func (state State) ToGrid() [][]string {
	// get boundaries
	maxx := 0
	maxy := 0
	for coord, _ := range state.Rooms {
		if coord.I > maxx {
			maxx = coord.I
		}
		if coord.J > maxy {
			maxy = coord.J
		}
	}
	maxx += 2
	maxy += 2
	// create grid full of walls
	var grid [][]string
	for j := 0; j < maxy; j++ {
		var row []string
		for i := 0; i < maxx; i++ {
			row = append(row, "#")
		}
		grid = append(grid, row)
	}
	// add each room to the grid
	for coord, room := range state.Rooms {
		grid[coord.J][coord.I] = room.Value
	}
	return grid
}

func (state State) PrintRooms() {
	grid := state.ToGrid()
	// print
	for _, row := range grid {
		for _, item := range row {
			fmt.Printf("%v", item)
		}
		fmt.Print("\n")
	}
	fmt.Print("\n")
}

func ReadInput(path string) State {
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
	rooms := make(map[utils.Coord]Room)
	for j, line := range lines {
		for i, char := range line {
			room := Room{Rtype: Hallway, Value: "."}
			if char != '#' {
				if char == '.' {
					if i == 3 || i == 5 || i == 7 || i == 9 {
						room.Rtype = Doorway
					} else {
						room.Rtype = Hallway
					}
				} else {
					// it's a letter in a room
					// save the room
					if j == 2 || j == 3 {
						if i == 3 {
							room.Rtype = ARoom
						} else if i == 5 {
							room.Rtype = BRoom
						} else if i == 7 {
							room.Rtype = CRoom
						} else if i == 9 {
							room.Rtype = DRoom
						}
					}
				}
				// save the letter
				room.Value = string(char)
				rooms[utils.Coord{I: i, J: j}] = room
				// rooms = append(rooms, room)
			} // else, it's a wall
		}
	}

	return State{Rooms: rooms, Cost: 0}
}
