package day08

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type InputRow struct {
	SignalPatterns []string
	OutputValues   []string
}

func ReadInput(path string) []InputRow {
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

	var input []InputRow
	for _, line := range lines {
		signalOutputSplit := strings.Split(line, " | ")
		if len(signalOutputSplit) < 2 {
			panic(fmt.Errorf("could not parse input line: %v", line))
		}
		signalStr := signalOutputSplit[0]
		outputStr := signalOutputSplit[1]
		inputRow := InputRow{strings.Split(signalStr, " "), strings.Split(outputStr, " ")}
		input = append(input, inputRow)
	}

	return input
}
