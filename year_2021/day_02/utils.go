package day02

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Command struct {
	Direction string
	Amount    int
}

func PrintCommands(commands []Command) {
	for _, c := range commands {
		fmt.Printf("%v\n", c)
	}
}

func ReadInput(path string) ([]Command, error) {
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

	var commands []Command
	for _, l := range lines {
		var split = strings.Split(l, " ")
		if len(split) < 2 {
			panic("input could not be parsed")
		}
		direction := split[0]
		amount, err := strconv.Atoi(split[1])
		if err != nil {
			panic(err)
		}
		commands = append(commands, Command{Direction: direction, Amount: amount})
	}
	return commands, scanner.Err()
}
