package main

import (
	"fmt"
	"os"
	day19 "year_2021/day_19"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	scanners := day19.ReadInput(os.Args[1])
	// fmt.Printf("Input: %v\n", scanners)
	var baseCoords []day19.Coord3d
	// maxScanners := len(scanners)

	// Add scanner 0 coords to base
	baseCoords = append(baseCoords, scanners[0]...)

	// Save off all scanner rotations for reuse
	scannerRotations := make(map[int]map[int][]day19.Coord3d)
	for i := range scanners {
		scannerRotations[i] = day19.GetAllScannerRotations(scanners[i])
	}

	// Until we've exhausted all the scanners
	for {
		if len(scanners) <= 0 {
			break
		}
		// For each remaining scanner
		for i := range scanners {
			// Get all the rotations
			scannerRotations := scannerRotations[i]
			// For each rotation
			for _, rotation := range scannerRotations {
				// Try to find the translation if there are 12 overlapping distances
				translation := day19.FindTranlationIfOverlap(baseCoords, rotation)
				// fmt.Printf("translation between base with %v: %v", i, translation)
				// If there is one, add the translated coords to the base
				if translation != nil {
					baseCoords = append(baseCoords, day19.TranslateScannerBeacons(rotation, *translation)...)
					delete(scanners, i)
				}
			}
		}
	}
	// Convert to a map to remove duplicates
	baseMap := make(map[day19.Coord3d]int, 0)
	for _, b := range baseCoords {
		baseMap[b] = 0
	}

	for b, _ := range baseMap {
		fmt.Printf("%v\n", b)
	}

	fmt.Printf("Result: %v\n", len(baseMap))
}
