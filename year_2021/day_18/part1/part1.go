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
	trees := day18.ReadInput(os.Args[1])

	tree := trees[0]
	for i := 1; i < len(trees); i++ {
		// Add the next tree
		newTree := day18.CombineTwoTrees(tree, trees[i])
		tree = newTree
		// Print it
		day18.PrintPostOrder(tree.Root)
		fmt.Print("\n")

		// Loop until we can't explode or split
		for {
			explodeNode := tree.Root.CanExplode(0)
			splitNode := tree.Root.CanSplit()
			if explodeNode == nil && splitNode == nil {
				break
			}
			// Prioritize exploding
			if explodeNode != nil {
				fmt.Printf("Exploding: %v -> ", explodeNode)
				explodeNode.Explode()
				day18.PrintPostOrder(tree.Root)
				fmt.Print("\n")
				continue
			}
			if splitNode != nil {
				fmt.Printf("Splitting: %v     -> ", splitNode)
				splitNode.Split()
			}
			day18.PrintPostOrder(tree.Root)
			fmt.Print("\n")
		}
	}
	fmt.Print("Final sum: ")
	day18.PrintPostOrder(tree.Root)
	fmt.Print("\n")
	// Check magnitude
	fmt.Printf("Magnitude: %v\n", day18.Magnitude(tree.Root))
}
