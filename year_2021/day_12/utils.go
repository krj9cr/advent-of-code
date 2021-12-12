package day12

import (
	"bufio"
	"log"
	"os"
	"strings"
	"unicode"
)

func ReadInput(path string) *Graph {
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

	g := NewUndirectedGraph()
	for _, line := range lines {
		lineSplit := strings.Split(line, "-")
		// Add nodes
		for _, item := range lineSplit {
			g.AddVertex(item)
		}
		// Add edges
		if len(lineSplit) < 2 {
			log.Panicf("Could not parse line: %v", line)
		}
		item1 := lineSplit[0]
		item2 := lineSplit[1]

		// fmt.Printf("Adding edge: %v -> %v\n", item1, item2)
		g.AddEdge(item1, item2)
	}

	return g
}

func IsUpper(s string) bool {
	for _, r := range s {
		if !unicode.IsUpper(r) && unicode.IsLetter(r) {
			return false
		}
	}
	return true
}
