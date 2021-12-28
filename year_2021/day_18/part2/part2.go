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

	maxMag := 0
	var maxSum *day18.Tree
	for i := 0; i < len(trees); i++ {
		for j := 0; j < len(trees); j++ {
			if i == j {
				continue
			}
			treeA := trees[i]
			treeB := trees[j]
			// Add the trees
			tree := day18.CombineTwoTrees(treeA, treeB)
			// fmt.Printf("%v\n\n", tree)

			// Loop until we can't explode or split
			for {
				// Reparse tree bc i stink at pointers
				root := &day18.BinaryNode{Parent: nil, Left: nil, Right: nil, Data: nil}
				newTree := &day18.Tree{Root: root}
				day18.ParseExpr(root, fmt.Sprintf("%v", tree))
				tree = newTree

				// Recompute adj list
				adjArr := tree.Root.AdjacencyArrayWithDepth(0)
				// fmt.Printf("Adjarr: %v\n", adjArr)

				// Check if we can explode or split
				explodeNode := day18.CanExplode(adjArr)
				splitNode := day18.CanSplit(adjArr)
				// fmt.Printf("ExplodeNode: %v, splitNode: %v\n", explodeNode, splitNode)
				if explodeNode == nil && splitNode == nil {
					break
				}
				// Prioritize exploding
				if explodeNode != nil {
					// fmt.Printf("Exploding: %v -> ", explodeNode)
					explodeNode.Explode(adjArr)
					// day18.PrintPostOrder(tree.Root)
					// fmt.Print("\n\n")
					continue
				}
				if splitNode != nil {
					// fmt.Printf("Splitting: %v     -> ", splitNode)
					splitNode.Split()
				}
				// fmt.Printf("%v\n\n", tree)
			}
			// fmt.Printf("Final sum: %v\n\n", tree)
			// Check magnitude
			mag := day18.Magnitude(tree.Root)
			// fmt.Printf("Magnitude: %v\n", mag)
			if mag > maxMag {
				maxMag = mag
				maxSum = tree
			}
		}
	}
	fmt.Printf("MAX Tree: %v\nMAX Magnitude: %v\n", maxSum, maxMag)
}
