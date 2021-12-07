package main

import (
	"fmt"
	"os"
	day06 "year_2021/day_06"
)

func countFish(fishMap map[int]int) int {
	count := 0
	for _, val := range fishMap {
		count += val
	}
	return count
}

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	fish := day06.ReadInput(os.Args[1])
	fmt.Printf("Input: %v\n", fish)

	numDays := 256
	spawnDays := 6
	initialDays := 8

	// Keep track in a MAP of how many fish are at each spawn time
	// save on memory lul
	fishMap := make(map[int]int)
	spawnKeys := make([]int, 0)
	// init map
	for i := initialDays; i >= 0; i-- {
		fishMap[i] = 0
		spawnKeys = append(spawnKeys, i)
	}
	for _, f := range fish {
		fishMap[f] += 1
	}

	fmt.Printf("Spawn keys: %v", spawnKeys)
	fmt.Printf("Initial size: %v, %v\n", countFish(fishMap), fishMap)
	for day := 1; day <= numDays; day++ {
		newMap := make(map[int]int)
		for spawn := range fishMap {
			newMap[spawn] = 0
		}
		// For each number of spawn days
		for _, spawn := range spawnKeys {
			// fmt.Printf("Checking spawn: %v, numFish: %v\n", spawn, numFish)
			// Check if spawn
			if spawn == 0 {
				newMap[initialDays] = fishMap[spawn]
				newMap[spawnDays] = fishMap[spawnDays+1] + fishMap[spawn]
			} else {
				newMap[spawn-1] = fishMap[spawn]
			}
			// fmt.Printf("Fish:    %v\nNewFish: %v\n", fishMap, newMap)
		}
		for spawn, numFish := range newMap {
			fishMap[spawn] = numFish
		}

		// fmt.Printf("After %v day, size %v\n", day, countFish(fishMap))
		// fmt.Printf("%v\n", fishMap)
	}

	fmt.Printf("Day: %v, %v\n", numDays, countFish(fishMap))
}
