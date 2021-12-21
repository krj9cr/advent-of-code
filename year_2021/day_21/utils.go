package day21

import (
	"bufio"
	"log"
	"os"
	"strconv"
	"strings"
)

func ReadInput(path string) (int, int) {
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

	if len(lines) != 2 {
		log.Panicf("could not read input\n")
	}

	p1 := strings.Split(lines[0], " ")[4]
	p2 := strings.Split(lines[1], " ")[4]

	i1, err := strconv.Atoi(p1)
	if err != nil {
		panic(err)
	}
	i2, err := strconv.Atoi(p2)
	if err != nil {
		panic(err)
	}

	return i1, i2
}
