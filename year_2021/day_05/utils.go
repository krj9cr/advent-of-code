package day05

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

type Point struct {
	x int
	y int
}

func (p Point) String() string {
	return fmt.Sprintf("(%v, %v)", p.x, p.y)
}

type LineSegment struct {
	a Point
	b Point
}

func (l LineSegment) String() string {
	return fmt.Sprintf("%v -> %v", l.a, l.b)
}

// Returns minx, maxx, miny, maxy
func FindMinMaxCoords(lineSegments []LineSegment) (int, int, int, int) {
	minx := 0
	maxx := 0
	miny := 0
	maxy := 0
	for _, lineSegment := range lineSegments {
		if lineSegment.a.x > maxx {
			maxx = lineSegment.a.x
		}
		if lineSegment.b.x > maxx {
			maxx = lineSegment.b.x
		}
		if lineSegment.a.y > maxy {
			maxy = lineSegment.a.y
		}
		if lineSegment.b.y > maxy {
			maxy = lineSegment.b.y
		}
	}
	return minx, maxx, miny, maxy
}

func (l LineSegment) Slope() (int, int, float64, error) {
	rise := (l.b.y - l.a.y)
	run := (l.b.x - l.a.x)
	if run == 0 {
		return rise, run, 0, fmt.Errorf("slope is undefined")
	}
	return rise, run, float64(rise) / float64(run), nil
}

func (l LineSegment) GeneratePoints(includeDiagonal bool) []Point {
	var points []Point

	currX := l.a.x
	currY := l.a.y

	rise, run, slope, err := l.Slope()
	if err != nil {
		// Undefined slope means it's a vertical line
		if l.b.y-l.a.y < 0 {
			currX = l.b.x
			currY = l.b.y
			height := l.a.y - l.b.y
			for i := 0; i < height+1; i++ {
				currY := currY + i
				points = append(points, Point{currX, currY})
			}
		} else {
			height := l.b.y - l.a.y
			for i := 0; i < height+1; i++ {
				currY := currY + i
				points = append(points, Point{currX, currY})
			}
		}
	} else {
		// It has a defined slope
		if includeDiagonal || slope == 0 {
			if l.b.x-l.a.x < 0 {
				currX = l.b.x
				currY = l.b.y
				width := l.a.x - l.b.x
				for i := 0; i < width+1; i++ {
					currX := currX + i
					currY := currY + int((slope * float64(i)))
					points = append(points, Point{currX, currY})
				}
			} else {
				width := l.b.x - l.a.x
				for i := 0; i < width+1; i++ {
					currX := currX + i
					currY := currY + int((slope * float64(i)))
					points = append(points, Point{currX, currY})
				}
			}
		}
	}
	fmt.Printf("Line segment %v, rise: %v, run: %v, slope: %v-%v\n", l, rise, run, slope, err)

	return points
}

func (l LineSegment) Chart(grid [][]int, includeDiagonal bool) {
	points := l.GeneratePoints(includeDiagonal)
	fmt.Printf("Line segment %v; Generated points: %v\n", l, points)
	for _, point := range points {
		grid[point.y][point.x] += 1
	}
}

func ReadInput(path string) []LineSegment {
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

	var lineSegments []LineSegment
	for _, line := range lines {
		coords := strings.Split(line, " -> ")
		if len(coords) < 2 {
			log.Panicf("Could not parse coords: %v", coords)
		}
		a := coords[0]
		b := coords[1]
		aNums := strings.Split(a, ",")
		bNums := strings.Split(b, ",")

		a1, err := strconv.Atoi(aNums[0])
		if err != nil {
			panic(err)
		}
		a2, err := strconv.Atoi(aNums[1])
		if err != nil {
			panic(err)
		}
		b1, err := strconv.Atoi(bNums[0])
		if err != nil {
			panic(err)
		}
		b2, err := strconv.Atoi(bNums[1])
		if err != nil {
			panic(err)
		}
		aPoint := Point{a1, a2}
		bPoint := Point{b1, b2}
		lineSegments = append(lineSegments, LineSegment{aPoint, bPoint})
	}

	return lineSegments
}
