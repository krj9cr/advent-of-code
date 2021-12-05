package utils

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
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

func PrintGrid(slice [][]int) {
	for _, row := range slice {
		for _, item := range row {
			fmt.Printf("%v ", item)
		}
		fmt.Print("\n")
	}
	fmt.Print("\n")
}

// writeLines writes the lines to the given file.
func WriteLines(lines []string, path string) error {
	file, err := os.Create(path)
	if err != nil {
		return err
	}
	defer file.Close()

	w := bufio.NewWriter(file)
	for _, line := range lines {
		fmt.Fprintln(w, line)
	}
	return w.Flush()
}
