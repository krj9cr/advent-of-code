package day15

import (
	"container/heap"
	"math"
	"year_2021/utils"
)

type Coord struct {
	I int
	J int
}

// guesses the cost of going from current position to goal
// should always underestimate the actual cost
func heuristic(goal Coord, x2 int, y2 int) int {
	x1 := goal.I
	y1 := goal.J
	dist := math.Abs(float64(x1)-float64(x2)) + math.Abs(float64(y1)-float64(y2))
	return int(dist)
}

func Astar(grid [][]int, start Coord, end Coord) (map[Coord]*Coord, map[Coord]int) {
	// init
	pq := make(PriorityQueue, 0)

	came_from := map[Coord]*Coord{} // keeps track of our path to the goal
	cost_so_far := map[Coord]int{}  // keeps track of cost to arrive at ((x, y))

	// add start infos
	item := &Item{
		Value:    start,
		Priority: 0,
	}
	heap.Push(&pq, item)
	came_from[start] = nil
	cost_so_far[start] = 0
	heap.Init(&pq)

	// while queue not empty
	for ok := true; ok; ok = pq.Len() > 0 {
		// sort heap
		heap.Init(&pq)
		// fmt.Printf("Popped item: %v\n", item)
		item := heap.Pop(&pq).(*Item)
		x := item.Value.I
		y := item.Value.J
		currCoord := item.Value

		if x == end.I && y == end.J {
			// fmt.Printf("Landed at end!\n")
			break
		}

		// for each adjacent square
		neighbors := utils.GetCardinalNeighbors(grid, x, y)
		for _, neighbor := range neighbors {
			x2 := neighbor.I
			y2 := neighbor.J
			// if we're not out of bounds
			if 0 <= y2 && y2 < len(grid) && 0 <= x2 && x2 < len(grid[y2]) {
				cost_to_move := grid[y2][x2] // note this could vary on implementation
				new_cost := cost_so_far[currCoord] + cost_to_move
				next_spot := Coord{x2, y2}
				// if next_spot in cost_so_far, continue
				found := false
				for key := range cost_so_far {
					if key == next_spot {
						found = true
						break
					}
				}
				// if it's cheap to move
				if !found || new_cost < cost_so_far[next_spot] {
					cost_so_far[next_spot] = new_cost
					priority := new_cost + heuristic(end, x2, y2)
					item := &Item{
						Value:    next_spot,
						Priority: priority,
					}
					heap.Push(&pq, item)
					came_from[next_spot] = &currCoord
				}
			}
		}
	}
	return came_from, cost_so_far
}
