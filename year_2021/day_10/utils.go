package day10

import (
	"bufio"
	"fmt"
	"os"
)

type Stack []rune

func (s Stack) Push(v rune) Stack {
	return append(s, v)
}

func (s Stack) Pop() (Stack, *rune) {
	l := len(s)
	if l == 0 {
		return s, nil
	}
	return s[:l-1], &s[l-1]
}

// Return error if line is bad
// return the character the line is bad on, too, only if error
func CheckLineSyntax(line string) (error, rune, Stack) {
	stack := make(Stack, 0)
	for i, char := range line {

		// for _, s := range stack {
		// 	fmt.Printf("%v ", string(s))
		// }
		// fmt.Printf("  current char: %v at %v\n", string(char), i)

		if char == '(' || char == '[' || char == '{' || char == '<' {
			stack = stack.Push(char)
		} else { // Assume it's one of the closing brackets
			s, lastPtr := stack.Pop()
			// _ = stack // ignore unused stack
			if lastPtr == nil {
				panic(fmt.Errorf("uh oh, stack is empty"))
			}
			if char == ')' && *lastPtr != '(' {
				return fmt.Errorf("expected match for %v, but found %v instead (index %v)", string(*lastPtr), string(char), i), char, stack
			} else if char == ']' && *lastPtr != '[' {
				return fmt.Errorf("expected match for %v, but found %v instead (index %v)", string(*lastPtr), string(char), i), char, stack
			} else if char == '}' && *lastPtr != '{' {
				return fmt.Errorf("expected match for %v, but found %v instead (index %v)", string(*lastPtr), string(char), i), char, stack
			} else if char == '>' && *lastPtr != '<' {
				return fmt.Errorf("expected match for %v, but found %v instead (index %v)", string(*lastPtr), string(char), i), char, stack
			}
			stack = s
		}
	}
	if len(stack) > 0 {
		return fmt.Errorf("stack still contains values"), 0, stack
	}
	return nil, 0, stack
}

func AutocompleteStack(stack Stack) []rune {
	var runes []rune
	for ok := true; ok; ok = len(stack) > 0 {
		s, item := stack.Pop()
		if item == nil {
			panic(fmt.Errorf("uh oh, somehow we popped but the stack was empty"))
		}
		stack = s
		if *item == '(' {
			runes = append(runes, ')')
		} else if *item == '[' {
			runes = append(runes, ']')
		} else if *item == '{' {
			runes = append(runes, '}')
		} else if *item == '<' {
			runes = append(runes, '>')
		} else {
			panic(fmt.Errorf("uh oh, unknown item: %v", string(*item)))
		}
	}
	return runes
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
