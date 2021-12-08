package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
	day08 "year_2021/day_08"
)

type EntryPair struct {
	Entry1 string
	Entry2 string
	Matches int
}

func findNumMatching(entry1 string, entry2 string) int {
	count := 0
	for _, char := range entry1 {
		if strings.Contains(entry2, string(char)) {
			count += 1
		}
	}
	return count
}

func allMatching(entry1 string, entry2 string) bool {
	if len(entry1) != len(entry2) {
		return false
	} else {
		if findNumMatching(entry1, entry2) == len(entry2) {
			return true
		} else {
			return false
		}
	}
}

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	inputRows := day08.ReadInput(os.Args[1])
	// fmt.Printf("Input: %v\n", inputRows)

	// DO STUFF
	sum := 0
	for _, row := range inputRows {

		entryMap := make(map[string]int)
		var fivers []string
		var sixers []string
		for _, entry := range row.SignalPatterns {
			numDigits := len(entry)
			if numDigits == 2 {
				entryMap[entry] = 1
			} else if numDigits == 3 {
				entryMap[entry] = 7
			} else if numDigits == 4 {
				entryMap[entry] = 4
			} else if numDigits == 7 {
				entryMap[entry] = 8
			} else if numDigits == 5 { // 2, 3, or 5
				fivers = append(fivers, entry)
			} else if numDigits == 6 { // 0, 6, or 9
				sixers = append(sixers, entry)
			}
		}
		// Figure out 2,3,5
		var fiverMatches []EntryPair
		for i, fiver := range fivers {
			for j, fiver2 := range fivers {
				if i < j {
					numMatches := findNumMatching(fiver, fiver2)
					fiverMatches = append(fiverMatches, EntryPair{fiver, fiver2, numMatches})
				}
			}
		}
		//fmt.Printf("Fiver matches: %v\n", fiverMatches)
		// Find the entry that has two 4 matches
		var entry3 string
		var fiverMatchWithFour []string
		for _, fiverMatch := range fiverMatches {
			if fiverMatch.Matches == 4 {
				for _, existingMatch := range fiverMatchWithFour {
					if existingMatch == fiverMatch.Entry1 {
						entry3 = existingMatch
						break
					} else if existingMatch == fiverMatch.Entry2 {
						entry3 = existingMatch
						break
					}
				}
				fiverMatchWithFour = append(fiverMatchWithFour, fiverMatch.Entry1)
				fiverMatchWithFour = append(fiverMatchWithFour, fiverMatch.Entry2)
			}
		}
		if entry3 == "" {
			panic(fmt.Errorf("could not find entry for 3?? %v", row))
		}
		entryMap[entry3] = 3

		var twoOrFive []string
		for _, fiver := range fivers {
			if fiver != entry3 {
				twoOrFive = append(twoOrFive, fiver)
			}
		}

		//fmt.Printf("Entrymap: %v; twoOrFive: %v; sixers: %v\n", entryMap, twoOrFive, sixers)

		// 2 should have exactly 2 matches with 4, and 5 should have exactly 3
		var two string
		var five string
		for _, entry := range twoOrFive {
			for key, value := range entryMap {
				if value == 4 {
					if findNumMatching(entry, key) == 2 {
						two = entry
					} else {
						five = entry
					}
				}
			}
		}
		if two == ""  || five == "" {
			panic(fmt.Errorf("could not find entry for 2 or 5?? %v\n", row))
		}
		entryMap[two] = 2
		entryMap[five] = 5

		// 9 should have 5 matches with 3
		var nine string
		for _, sixer := range sixers {
			for key, value := range entryMap {
				if value == 3 {
					if findNumMatching(sixer, key) == 5 {
						nine = sixer
						break
					}
				}
			}
		}
		if nine == "" {
			panic(fmt.Errorf("could not find entry for 0?? %v\n", row))
		}
		entryMap[nine] = 9

		// 0 is whichever sixer is left that has 2 matches with 1
		var zero string
		for _, sixer := range sixers {
			if sixer != nine {
				for key, value := range entryMap {
					if value == 1 {
						if findNumMatching(sixer, key) == 2 {
							zero = sixer
							break
						}
					}
				}
			}
		}
		if zero == "" {
			panic(fmt.Errorf("could not find entry for 0?? %v\n", row))
		}
		entryMap[zero] = 0

		// 6 is whichever sixer is left
		var six string
		for _, sixer := range sixers {
			if sixer != zero && sixer != nine {
				six = sixer
				break
			}
		}
		if zero == "" {
			panic(fmt.Errorf("could not find entry for 6?? %v\n", row))
		}
		entryMap[six] = 6


		//fmt.Printf("Entrymap: %v", entryMap)

		var valueStr string
		// For each outputValue, check if it has the same letters contained
		// as one of the keys in entryMap to determine its number
		for _, entry := range row.OutputValues {
			 for key, value := range entryMap {
				 if  allMatching(entry, key) {
					 valueStr += strconv.Itoa(value)
					 //fmt.Printf("entry: %v; has value: %v\n", entry, value)
					 break
				 }
			 }
		}
		value, err := strconv.Atoi(valueStr)
		if err != nil {
			panic(err)
		}
		//fmt.Printf("%v outputValues: %v: %v\n", i, row.OutputValues, value)
		sum += value
	}

	fmt.Printf("Result: %v\n", sum)
}
