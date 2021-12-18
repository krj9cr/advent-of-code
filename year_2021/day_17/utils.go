package day17

import (
	"bufio"
	"os"
	"strconv"
	"strings"
	"year_2021/utils"
)

type TargetArea struct {
	XMin int
	XMax int
	YMin int
	YMax int
}

type Velocity struct {
	X int
	Y int
}

// Figure out if Coord is within TargetArea
func IntersectArea(targetArea TargetArea, coord utils.Coord) bool {
	return coord.I >= targetArea.XMin && coord.I <= targetArea.XMax && coord.J >= targetArea.YMin && coord.J <= targetArea.YMax
}

// Detect if x or y are beyond the target area?
// Assumes target area is to the right and below the start point (0,0)
func OverShotArea(targetArea TargetArea, coord utils.Coord) bool {
	return coord.I > targetArea.XMax || coord.J < targetArea.YMin
}

func ChangeVelocity(velocity Velocity) Velocity {
	var newX int
	newY := velocity.Y - 1

	if velocity.X > 0 {
		newX = velocity.X - 1
	} else if velocity.X == 0 {
		newX = 0
	} else {
		newX = velocity.X + 1
	}
	return Velocity{newX, newY}
}

// Return whether we interesect with target area at some point, and max height
func RunSim(targetArea TargetArea, initialVelocity Velocity) (bool, int) {
	curr := utils.Coord{I: 0, J: 0}
	velocity := initialVelocity
	maxHeight := 0
	// Forever
	for {
		// fmt.Printf("Curr: %v\n", curr)
		// Until the current location intersects or is beyond the target area
		if IntersectArea(targetArea, curr) {
			// fmt.Printf("%v intersects area\n", curr)
			break
		}
		if OverShotArea(targetArea, curr) {
			// fmt.Printf("%v overshot area\n", curr)
			break
		}
		// Move the curr coord according to velocity
		curr = utils.Coord{I: curr.I + velocity.X, J: curr.J + velocity.Y}
		// Adjust velocity
		v := ChangeVelocity(velocity)
		velocity = v
		// Check max height
		if curr.J > maxHeight {
			maxHeight = curr.J
		}
	}
	return IntersectArea(targetArea, curr), maxHeight
}

// target area: x=20..30, y=-10..-5
// Returns, xmin, xmas, ymin, ymax
func ReadInput(path string) TargetArea {
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

	line := lines[0]
	splitSpace := strings.Split(line, " ")
	xStr := strings.TrimPrefix(splitSpace[2], "x=")
	xStr = strings.TrimSuffix(xStr, ",")
	yStr := strings.TrimPrefix(splitSpace[3], "y=")

	xNums := strings.Split(xStr, "..")
	yNums := strings.Split(yStr, "..")

	xmin, err := strconv.Atoi(xNums[0])
	if err != nil {
		panic(err)
	}
	xmax, err := strconv.Atoi(xNums[1])
	if err != nil {
		panic(err)
	}

	ymin, err := strconv.Atoi(yNums[0])
	if err != nil {
		panic(err)
	}
	ymax, err := strconv.Atoi(yNums[1])
	if err != nil {
		panic(err)
	}

	return TargetArea{xmin, xmax, ymin, ymax}
}
