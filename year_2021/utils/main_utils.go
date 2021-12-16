package utils

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

// readLines reads a whole file into memory
// and returns a slice of its lines.
func ReadLinesToStrings(path string) ([]string, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	return lines, scanner.Err()
}

func ReadLinesToStringGrid(path string, splitter string) [][]string {
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

	var grid [][]string
	for _, line := range lines {
		var row []string
		for _, l := range strings.Split(line, splitter) {
			row = append(row, string(l))
		}
		grid = append(grid, row)
	}

	return grid
}

func ReadLinesToIntGrid(path string, splitter string) [][]int {
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

	var grid [][]int
	for _, line := range lines {
		var row []int
		for _, l := range strings.Split(line, splitter) {
			intval, err := strconv.Atoi(l)
			if err != nil {
				log.Panicf("could not parse int %v in line: %v", l, line)
			}
			row = append(row, intval)
		}
		grid = append(grid, row)
	}

	return grid
}

func ReadLinesToInts(path string) ([]int, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	var ints []int
	for _, l := range lines {
		var intval, err = strconv.Atoi(l)
		if err != nil {
			panic(err)
		}
		ints = append(ints, intval)
	}
	return ints, scanner.Err()
}

func PrintStringSlice(slice []string) {
	for _, s := range slice {
		fmt.Printf("%v\n", s)
	}
}

func PrintIntSlice(slice []int) {
	for _, s := range slice {
		fmt.Printf("%d\n", s)
	}
}
