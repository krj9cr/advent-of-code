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

	// Use a map to remove duplicates
	baseCoords := make(map[day19.Coord3d]int)
	// maxScanners := len(scanners)

	// Add scanner 0 coords to base
	for _, b := range scanners[0] {
		baseCoords[b] = 0
	}
	delete(scanners, 0)

	// Until we've exhausted all the scanners
	for {
		if len(scanners) <= 0 {
			break
		}
		if len(baseCoords) > 392 {
			break
		}
		// For each remaining scanner
		for i := range scanners {
			// fmt.Printf("scanner: %v\n", i)
			// Get all the rotations
			scannerRotations := day19.GetAllScannerRotations(scanners[i])
			// For each rotation
			for _, rotation := range scannerRotations {
				// Try to find the translation if there are 12 overlapping distances
				baseCoordsKeys := make([]day19.Coord3d, 0, len(baseCoords))
				for c := range baseCoords {
					baseCoordsKeys = append(baseCoordsKeys, c)
				}
				translation := day19.FindTranlationIfOverlap(baseCoordsKeys, rotation)
				// If there is one, add the translated coords to the base
				if translation != nil {
					// fmt.Printf("translation between base with %v: %v\n", i, translation)
					for _, b := range day19.TranslateScannerBeacons(rotation, *translation) {
						baseCoords[b] = 0
					}
					delete(scanners, i)
					break
				}
			}
		}
	}

	fmt.Printf("Result: %v\n", len(baseCoords))
}
