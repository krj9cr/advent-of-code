package day07

import (
	"bufio"
	"os"
	"strconv"
	"strings"
)

func ReadInput(path string) []int {
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

	var ints []int
	strs := strings.Split(lines[0], ",")
	for _, str := range strs {
		intval, err := strconv.Atoi(str)
		if err != nil {
			panic(err)
		}
		ints = append(ints, intval)
	}

	return ints
}
