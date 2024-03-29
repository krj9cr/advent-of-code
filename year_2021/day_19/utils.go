package day19

import (
	"bufio"
	"math"
	"os"
	"strconv"
	"strings"
)

type Coord3d struct {
	X int
	Y int
	Z int
}

func (coordA Coord3d) Add(coordB Coord3d) Coord3d {
	return Coord3d{X: coordA.X + coordB.X, Y: coordA.Y + coordB.Y, Z: coordA.Z + coordB.Z}
}

func (coordA Coord3d) Dist(coordB Coord3d) Coord3d {
	return Coord3d{X: coordA.X - coordB.X, Y: coordA.Y - coordB.Y, Z: coordA.Z - coordB.Z}
}

func (coordA Coord3d) ManattanDist(coordB Coord3d) int {
	return int(math.Abs(float64(coordA.X)-float64(coordB.X))) +
		int(math.Abs(float64(coordA.Y)-float64(coordB.Y))) +
		int(math.Abs(float64(coordA.Z)-float64(coordB.Z)))
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

func FindTranlationIfOverlap(scannerA []Coord3d, scannerB []Coord3d) *Coord3d {
	distances := make(map[Coord3d]int, 0)
	for _, b1 := range scannerA {
		for _, b2 := range scannerB {
			// fmt.Printf("Cecking: %v, %v\n", b1, b2)
			dist := b1.Dist(b2)
			currDist := distances[dist]
			newDist := currDist + 1
			distances[dist] = newDist
			// Terminate early if we can
			if newDist >= 12 {
				return &dist
			}
		}
	}
	// fmt.Printf("distances: %v\n", distances)
	// for dist, count := range distances {
	// 	if count >= 12 {
	// 		return &dist
	// 	}
	// }
	return nil
}

// Add translated coords from scanner2 to scanner1, remove scanner2
func CombineScanners(scanner1 int, scanner2 int, translation Coord3d, scanners map[int][]Coord3d) {
	scanners[scanner1] = append(scanners[scanner1], TranslateScannerBeacons(scanners[scanner2], translation)...)
	delete(scanners, scanner2)
}

func TranslateScannerBeacons(beacons []Coord3d, translation Coord3d) []Coord3d {
	var result []Coord3d
	for _, coord := range beacons {
		result = append(result, coord.Add(translation))
	}
	return result
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
		{X: -coord.Z, Y: -coord.X, Z: +coord.Y},
		{X: -coord.Z, Y: +coord.Y, Z: +coord.X},
		{X: -coord.Z, Y: +coord.X, Z: -coord.Y},
		{X: -coord.Z, Y: -coord.Y, Z: -coord.X},
	}
}

// Take a list of scanner coords
// Return the 24 sets of rotations
func GetAllScannerRotations(coords []Coord3d) map[int][]Coord3d {
	result := make(map[int][]Coord3d)
	for _, coord := range coords {
		rots := GetAllCoordRotations(coord)
		// For each direction
		for i := 0; i < 24; i++ {
			result[i] = append(result[i], rots[i])
		}
	}
	return result
}
