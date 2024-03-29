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
	lines, err := utils.ReadLinesToStrings(os.Args[1])
	if err != nil {
		log.Fatalf("readLines: %s", err)
	}
	utils.PrintStringSlice(lines)
}
