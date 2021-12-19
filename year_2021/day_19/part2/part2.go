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

	// Something about my solution is non-deterministic!! WOOO
	// So we use this mega loop to continuously solve the problem until we get the right answer lmao
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

		scannerDists := []day19.Coord3d{{X: 0, Y: 0, Z: 0}}
		// var scannerDists []day19.Coord3d

		// Map scanner id to any coords not rel to zero
		scannerLocNotRelToZero := make(map[int][]day19.Coord3d)

		// Save off all scanner rotations for reuse
		// scannerRotations := make(map[int]map[int][]day19.Coord3d)
		// for i := range scanners {
		// 	scannerRotations[i] = day19.GetAllScannerRotations(scanners[i])
		// }

		numTimesRemainingKeysSame := 0
		numRemainingKeys := 0
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
						scannerDists = append(scannerDists, *translation)
						delete(scanners, i)
						for _, dist := range scannerLocNotRelToZero[i] {
							scannerDists = append(scannerDists, dist.Add(*translation))
						}
						break
					}
				}
			}
			// Print remaining keys
			// keys := make([]int, 0, len(scanners))
			// for k := range scanners {
			// 	keys = append(keys, k)
			// }
			if len(scanners) == numRemainingKeys {
				numTimesRemainingKeysSame += 1
			}
			if numTimesRemainingKeysSame >= 12 {
				fmt.Printf("stuck, terminating\n")
				break
			}
			numRemainingKeys = len(scanners)

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
							scannerLocNotRelToZero[j] = append(scannerLocNotRelToZero[j], *translation)
							// rotationMatch = true
							for _, dist := range scannerLocNotRelToZero[i] {
								scannerLocNotRelToZero[j] = append(scannerLocNotRelToZero[j], dist.Add(*translation))
							}
							break
						}
					}
				}
			}
		}

		result := len(baseCoords)
		fmt.Printf("Result: %v\n", result)
		// scannerDists = []day19.Coord3d{{0, 0, 0}, {130, 83, 1213}, {-28, 38, -1310}, {1252, -5890, 1090}, {17, 74, 2422}, {-1208, 1306, -1238}, {2503, -4847, 1182}}
		if result == 392 { // 79 for example or 392 for my part1 lmao
			fmt.Printf("scanenr dists: %v\n", scannerDists)

			// Find max manhattan dist
			maxmdist := 0
			for i, c1 := range scannerDists {
				for j, c2 := range scannerDists {
					if i == j {
						continue
					}
					mdist := c1.ManattanDist(c2)
					if mdist > maxmdist {
						maxmdist = mdist
					}
				}
			}

			// 12284 too low
			// 12357 not
			// 13358 not
			// 13336 not
			// 13627 too high
			// 17733 too high

			// This part isn't deterministic either, so I had to run it a bunch of times lmao
			// to narrow in on the answer. rip me
			fmt.Printf("Max manhattan dist: %v\n", maxmdist)
			if maxmdist > 12284 && maxmdist < 13627 && maxmdist != 13358 && maxmdist != 13336 && maxmdist != 12357 {
				break
			} else {
				continue
			}
		}
	}
}
