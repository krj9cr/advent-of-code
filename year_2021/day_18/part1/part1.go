package main

import (
	"fmt"
	"os"
	day18 "year_2021/day_18"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	tree := day18.ReadInput(os.Args[1])

	fmt.Printf("Input: ")
	day18.PrintPostOrder(tree.Root)
	fmt.Print("\n")

	// a := 88
	// b := 42
	// tree := day18.Tree{Root: &day18.BinaryNode{Parent: nil, Left: &day18.BinaryNode{Parent: nil, Left: nil, Right: nil, Data: &a}, Right: &day18.BinaryNode{Parent: nil, Left: nil, Right: nil, Data: &b}, Data: nil}}
	// fmt.Printf("Tree: %v\n", tree)

	// DO STUFF

	// fmt.Printf("Result: %v\n", result)
}
