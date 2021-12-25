package day24

import (
	"bufio"
	"log"
	"math/rand"
	"os"
	"strconv"
	"strings"
)

const inputLen = 14

func InputToNum(input []int) int {
	res := ""
	for _, in := range input {
		res += strconv.Itoa(in)
	}
	num, err := strconv.Atoi(res)
	if err != nil {
		panic(err)
	}
	return num
}

func NumToInput(in int) []int {
	str := strconv.Itoa(in)
	var res []int
	for _, char := range str {
		num, err := strconv.Atoi(string(char))
		if err != nil {
			panic(err)
		}
		res = append(res, num)
	}
	return res
}

func RandomInput() []int {
	result := make([]int, inputLen)
	result[0] = 9
	for i := 1; i < inputLen-1; i++ {
		result[i] = rand.Intn(10-1) + 1
	}
	return result
}

func ProcessLines(lines []string, input []int) map[string]int {
	variables := map[string]int{"w": 0, "x": 0, "y": 0, "z": 0}

	numInput := len(input)

	inpCounter := 0
	for _, line := range lines {
		var inp *int
		inp = nil
		if inpCounter < numInput {
			inp = &input[inpCounter]
		}
		wasInp := ProcessLine(line, variables, inp)
		if wasInp {
			inpCounter += 1
		}
	}
	return variables
}

// returns if it was an input line or not
func ProcessLine(line string, variables map[string]int, input *int) bool {
	splitLine := strings.Split(line, " ")
	if len(splitLine) < 2 {
		log.Panicf("could not parse line: %v\n", line)
	}
	command := splitLine[0]
	variable := splitLine[1]
	if command == "inp" {
		// TODO: read an input value and write it to variable
		if input == nil {
			log.Panicf("trying to process inp command: %v, but have no input\n", line)
		}
		variables[variable] = *input
		return true
	} else { // it has 3 items
		value, err := strconv.Atoi(splitLine[2])
		if err != nil {
			v, ok := variables[splitLine[2]]
			if !ok {
				log.Panicf("could not find variable %v\n", splitLine[2])
			}
			value = v
		}
		if command == "add" {
			variables[variable] += value
		} else if command == "mul" {
			variables[variable] *= value
		} else if command == "div" {
			newVal := int(float64(variables[variable]) / float64(value))
			variables[variable] = newVal
		} else if command == "mod" {
			variables[variable] %= value
		} else if command == "eql" {
			if variables[variable] == value {
				variables[variable] = 1
			} else {
				variables[variable] = 0
			}
		}
	}
	return false
}

func ReadInput(path string) []string {
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

	return lines
}
