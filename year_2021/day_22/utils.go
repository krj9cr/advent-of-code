package day22

import (
	"bufio"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
)

type Cube struct {
	Xmin, Xmax int
	Ymin, Ymax int
	Zmin, Zmax int
	On         bool
	Remove     []Cube
}

// If overlap, remove this cube
func (cube Cube) Combine(cube2 Cube) Cube {
	overlap := cube.GetOverlappingCube(cube2)
	if overlap != nil {
		return cube.RemoveCube(*overlap)
	}
	return cube
}

// When removing a cube, combine it with any other removed cubes to account for holes and things
func (cube Cube) RemoveCube(cube2 Cube) Cube {
	for i := range cube.Remove {
		r := cube.Remove[i]
		cube.Remove[i] = r.Combine(cube2)
	}
	cube.Remove = append(cube.Remove, cube2)
	return cube
}

func (cube Cube) Volume() int {
	w := cube.Xmax - cube.Xmin + 1
	h := cube.Ymax - cube.Ymin + 1
	l := cube.Zmax - cube.Zmin + 1
	base := w * h * l
	for _, removeCube := range cube.Remove {
		base -= removeCube.Volume()
	}
	return base
}

func (cubeA Cube) FullyContains(cubeB Cube) bool {
	x1 := cubeB.Xmin >= cubeA.Xmin
	x2 := cubeB.Xmax <= cubeA.Xmax

	y1 := cubeB.Ymin >= cubeA.Ymin
	y2 := cubeB.Ymax <= cubeA.Ymax

	z1 := cubeB.Zmin >= cubeA.Zmin
	z2 := cubeB.Zmax <= cubeA.Zmax

	return x1 && x2 && y1 && y2 && z1 && z2
}

func (cubeA Cube) GetOverlappingCube(cubeB Cube) *Cube {
	if cubeA.Overlaps(cubeB) {
		xmin := int(math.Max(float64(cubeA.Xmin), float64(cubeB.Xmin)))
		xmax := int(math.Min(float64(cubeA.Xmax), float64(cubeB.Xmax)))

		ymin := int(math.Max(float64(cubeA.Ymin), float64(cubeB.Ymin)))
		ymax := int(math.Min(float64(cubeA.Ymax), float64(cubeB.Ymax)))

		zmin := int(math.Max(float64(cubeA.Zmin), float64(cubeB.Zmin)))
		zmax := int(math.Min(float64(cubeA.Zmax), float64(cubeB.Zmax)))
		// We don't know what the On state is at this point, so set a default
		// I'm not sure that the state matters at this point, anyway
		return &Cube{xmin, xmax, ymin, ymax, zmin, zmax, true, []Cube{}}
	}
	return nil
}

// We use >= since the ranges are inclusive
func (cubeA Cube) Overlaps(cubeB Cube) bool {
	// Overlap in x
	x1 := (cubeA.Xmax >= cubeB.Xmin)
	x2 := (cubeA.Xmin <= cubeB.Xmax)
	// Overlap in y
	y1 := (cubeA.Ymax >= cubeB.Ymin)
	y2 := (cubeA.Ymin <= cubeB.Ymax)
	// Overlap in z
	z1 := (cubeA.Zmax >= cubeB.Zmin)
	z2 := (cubeA.Zmin <= cubeB.Zmax)
	return x1 && x2 && y1 && y2 && z1 && z2
}

// parses: x=10..12
func parseNum(s string) (int, int) {
	s = strings.TrimPrefix(s, "x=")
	s = strings.TrimPrefix(s, "y=")
	s = strings.TrimPrefix(s, "z=")
	nums := strings.Split(s, "..")
	if len(nums) != 2 {
		log.Panicf("could not parse num string: %v\n", s)
	}
	int1, err := strconv.Atoi(nums[0])
	if err != nil {
		panic(err)
	}
	int2, err := strconv.Atoi(nums[1])
	if err != nil {
		panic(err)
	}
	return int1, int2
}

func ReadInput(path string) []Cube {
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

	// parse into Cubes
	var cubes []Cube
	for _, line := range lines {
		spaceSplit := strings.Split(line, " ")
		if len(spaceSplit) != 2 {
			log.Panicf("could not split line by space: %v\n", line)
		}
		state := spaceSplit[0]
		on := false
		if state == "on" {
			on = true
		}
		commaSplit := strings.Split(spaceSplit[1], ",")
		if len(commaSplit) != 3 {
			log.Panicf("could not split line by comma: %v\n", line)
		}
		xmin, xmax := parseNum(commaSplit[0])
		ymin, ymax := parseNum(commaSplit[1])
		zmin, zmax := parseNum(commaSplit[2])
		cubes = append(cubes, Cube{xmin, xmax, ymin, ymax, zmin, zmax, on, []Cube{}})
	}

	return cubes
}
