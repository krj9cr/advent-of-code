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
	lines, err := utils.ReadLines(os.Args[1])
	if err != nil {
		log.Fatalf("readLines: %s", err)
	}
	utils.PrintSlice(lines)
}
