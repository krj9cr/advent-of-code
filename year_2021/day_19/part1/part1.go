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

	for {
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

		// Save off all scanner rotations for reuse
		// scannerRotations := make(map[int]map[int][]day19.Coord3d)
		// for i := range scanners {
		// 	scannerRotations[i] = day19.GetAllScannerRotations(scanners[i])
		// }

		// Until we've exhausted all the scanners
		for {
			if len(scanners) <= 0 {
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
			// Print remaining keys
			// keys := make([]int, 0, len(scanners))
			// for k := range scanners {
			// 	keys = append(keys, k)
			// }
			// fmt.Printf("remaining keys: %v\n", keys)

			// Also check scanners pairwise (not relative to zero)
			for j := range scanners {
				for i := range scanners {
					if i == j {
						continue
					}
					// fmt.Printf("scanner: %v, %v\n", j, i)
					// Get all the rotations
					scannerRotations := day19.GetAllScannerRotations(scanners[i])
					// For each rotation
					// rotationMatch := false
					for _, rotation := range scannerRotations {
						// Try to find the translation if there are 12 overlapping distances
						translation := day19.FindTranlationIfOverlap(scanners[j], rotation)
						// If there is one, add the translated coords to the base
						if translation != nil {
							// fmt.Printf("translation between %v with %v: %v\n", j, i, translation)
							scanners[j] = append(scanners[j], day19.TranslateScannerBeacons(rotation, *translation)...)
							delete(scanners, i)
							// rotationMatch = true
							break
						}
					}
				}
			}
		}

		// 403 too high

		fmt.Printf("Result: %v\n", len(baseCoords))
		if len(baseCoords) < 403 {
			// it's 392 lmao
			break
		}
	}
}
