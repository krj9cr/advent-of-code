package main

import (
	"fmt"
	"log"
	"os"
	"year_2021/utils"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	lines, err := utils.ReadLinesToInts(os.Args[1])
	if err != nil {
		log.Fatalf("readLines: %s", err)
	}
	utils.PrintIntSlice(lines)

	var count int = 0
	var size = len(lines)
	for i, l := range lines {
		if i+1 < size {
			var next = lines[i+1]
			if next > l {
				count += 1
			}
		}
	}
	fmt.Printf("Count: %v\n", count)
}
