package day14

import (
	"bufio"
	"log"
	"os"
	"strings"
)

type Polymer struct {
	Pair   string
	Insert string
}

func ReadInput(path string) (string, []Polymer) {
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

	var start string
	var polymers []Polymer
	for i, line := range lines {
		if i == 0 {
			start = line
		} else if i >= 2 {
			split := strings.Split(line, " -> ")
			if len(split) < 2 {
				log.Panicf("could not parse line %v", line)
			}
			polymers = append(polymers, Polymer{split[0], split[1]})
		}
	}

	return start, polymers
}
