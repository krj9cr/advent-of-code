package day19

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Coord3d struct {
	X int
	Y int
	Z int
}

func (coordA Coord3d) Dist(coordB Coord3d) Coord3d {
	return Coord3d{X: coordA.X - coordB.X, Y: coordA.Y - coordB.Y, Z: coordA.Z - coordB.Z}
}

func ReadInput(path string) map[int][]Coord3d {
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

	scanners := make(map[int][]Coord3d)
	currScanner := 0
	var beacons []Coord3d
	for _, line := range lines {
		if strings.Contains(line, "---") { // scanner line
			splitLine := strings.Split(line, " ")
			intval, err := strconv.Atoi(splitLine[2])
			if err != nil {
				panic(err)
			}
			// Add the current scanner to the map, before we reset it
			if intval != 0 {
				scanners[currScanner] = beacons
			}
			currScanner = intval
			beacons = []Coord3d{}
		} else if len(line) < 2 { // new line
			continue
		} else { // should contain beacon coords
			splitLine := strings.Split(line, ",")
			x, err := strconv.Atoi(splitLine[0])
			if err != nil {
				panic(err)
			}
			y, err := strconv.Atoi(splitLine[1])
			if err != nil {
				panic(err)
			}
			z, err := strconv.Atoi(splitLine[2])
			if err != nil {
				panic(err)
			}
			beacons = append(beacons, Coord3d{X: x, Y: y, Z: z})
		}
	}
	// Add the last scanner
	scanners[currScanner] = beacons

	return scanners
}

func FindOverlappingBeacons(scanner1 int, scanner2 int, scanners map[int][]Coord3d) *Coord3d {
	scannerRots := GetAllScannerRotations(scanners[scanner2])
	distances := make(map[Coord3d]int, 0)
	for _, coords := range scannerRots {
		for _, b1 := range scanners[scanner1] {
			for _, b2 := range coords {
				fmt.Printf("Cecking: %v, %v\n", b1, b2)

				dist := b1.Dist(b2)
				distances[dist] += 1
			}
		}
		fmt.Printf("distances: %v\n", distances)
		for dist, count := range distances {
			if count >= 12 {
				return &dist
			}
		}
	}
	return nil
}

func GetAllCoordRotations(coord Coord3d) []Coord3d {
	return []Coord3d{
		// positive x
		{X: +coord.X, Y: +coord.Y, Z: +coord.Z},
		{X: +coord.X, Y: -coord.Z, Z: +coord.Y},
		{X: +coord.X, Y: -coord.Y, Z: -coord.Z},
		{X: +coord.X, Y: +coord.Z, Z: -coord.Y},
		// negative x
		{X: -coord.X, Y: -coord.Y, Z: +coord.Z},
		{X: -coord.X, Y: +coord.Z, Z: +coord.Y},
		{X: -coord.X, Y: +coord.Y, Z: -coord.Z},
		{X: -coord.X, Y: -coord.Z, Z: -coord.Y},
		// positive y
		{X: +coord.Y, Y: +coord.Z, Z: +coord.X},
		{X: +coord.Y, Y: -coord.X, Z: +coord.Z},
		{X: +coord.Y, Y: -coord.Z, Z: -coord.X},
		{X: +coord.Y, Y: +coord.X, Z: -coord.Z},
		// negative y
		{X: -coord.Y, Y: -coord.Z, Z: +coord.X},
		{X: -coord.Y, Y: +coord.X, Z: +coord.Z},
		{X: -coord.Y, Y: +coord.Z, Z: -coord.X},
		{X: -coord.Y, Y: -coord.X, Z: -coord.Z},
		// positive z
		{X: +coord.Z, Y: +coord.X, Z: +coord.Y},
		{X: +coord.Z, Y: -coord.Y, Z: +coord.X},
		{X: +coord.Z, Y: -coord.X, Z: -coord.Y},
		{X: +coord.Z, Y: +coord.Y, Z: -coord.X},
		// negative z
		{X: -coord.Y, Y: -coord.X, Z: +coord.Y},
		{X: -coord.Y, Y: +coord.Y, Z: +coord.X},
		{X: -coord.Y, Y: +coord.X, Z: -coord.Y},
		{X: -coord.Y, Y: -coord.Y, Z: -coord.X},
	}
}

// Take a list of scanner coords
// Return the 24 sets of rotations
func GetAllScannerRotations(coords []Coord3d) map[int][]Coord3d {
	result := make(map[int][]Coord3d)
	for _, coord := range coords {
		rots := []Coord3d{
			// positive x
			{X: +coord.X, Y: +coord.Y, Z: +coord.Z},
			{X: +coord.X, Y: -coord.Z, Z: +coord.Y},
			{X: +coord.X, Y: -coord.Y, Z: -coord.Z},
			{X: +coord.X, Y: +coord.Z, Z: -coord.Y},
			// negative x
			{X: -coord.X, Y: -coord.Y, Z: +coord.Z},
			{X: -coord.X, Y: +coord.Z, Z: +coord.Y},
			{X: -coord.X, Y: +coord.Y, Z: -coord.Z},
			{X: -coord.X, Y: -coord.Z, Z: -coord.Y},
			// positive y
			{X: +coord.Y, Y: +coord.Z, Z: +coord.X},
			{X: +coord.Y, Y: -coord.X, Z: +coord.Z},
			{X: +coord.Y, Y: -coord.Z, Z: -coord.X},
			{X: +coord.Y, Y: +coord.X, Z: -coord.Z},
			// negative y
			{X: -coord.Y, Y: -coord.Z, Z: +coord.X},
			{X: -coord.Y, Y: +coord.X, Z: +coord.Z},
			{X: -coord.Y, Y: +coord.Z, Z: -coord.X},
			{X: -coord.Y, Y: -coord.X, Z: -coord.Z},
			// positive z
			{X: +coord.Z, Y: +coord.X, Z: +coord.Y},
			{X: +coord.Z, Y: -coord.Y, Z: +coord.X},
			{X: +coord.Z, Y: -coord.X, Z: -coord.Y},
			{X: +coord.Z, Y: +coord.Y, Z: -coord.X},
			// negative z
			{X: -coord.Y, Y: -coord.X, Z: +coord.Y},
			{X: -coord.Y, Y: +coord.Y, Z: +coord.X},
			{X: -coord.Y, Y: +coord.X, Z: -coord.Y},
			{X: -coord.Y, Y: -coord.Y, Z: -coord.X},
		}
		// For each direction
		for i := 0; i < 24; i++ {
			result[i] = append(result[i], rots[i])
		}
	}
	return result
}
