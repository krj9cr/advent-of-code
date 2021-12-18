package day18

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

type Tree struct {
	Root *BinaryNode
}

type BinaryNode struct {
	Parent *BinaryNode
	Left   *BinaryNode
	Right  *BinaryNode
	Data   *int
}

func PrintPostOrder(node *BinaryNode) {
	if node != nil {
		if node.Left != nil {
			fmt.Printf("[")
			PrintPostOrder(node.Left)
			if node.Left != nil && node.Left.Data != nil {
				fmt.Printf(",")
			}
		}
		if node.Right != nil {
			PrintPostOrder(node.Right)
			fmt.Printf("]")
			if node.Right != nil && node.Right.Data != nil {
				fmt.Printf(",")
			}
		}
		if node.Data != nil {
			fmt.Printf("%v", *node.Data)
		}
	}
}

func ParseExpr(parent *BinaryNode, expr string) {
	if len(expr) == 0 {
		return
	}
	first := expr[0]
	// it's either an int, or another expression!
	intval, err := strconv.Atoi(string(first))
	if err != nil { // it's another expression
		if first == '[' { // create and go to LEFT child
			child := &BinaryNode{Parent: parent, Left: nil, Right: nil, Data: nil}
			parent.Left = child
			ParseExpr(child, expr[1:])
		} else if first == ',' { // create and go to RIGHT child
			child := &BinaryNode{Parent: parent, Left: nil, Right: nil, Data: nil}
			parent.Right = child
			ParseExpr(child, expr[1:])
		} else if first == ']' { // move up to the PARENT
			ParseExpr(parent.Parent, expr[1:])
		}
	} else { // it's an int, stay
		parent.Data = &intval
		ParseExpr(parent.Parent, expr[1:])
	}
}

func ReadInput(path string) *Tree {
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

	var trees []*Tree
	// Parse each line into a tree
	for _, line := range lines {
		root := &BinaryNode{Parent: nil, Left: nil, Right: nil, Data: nil}
		tree := &Tree{Root: root}
		ParseExpr(root, line)
		trees = append(trees, tree)
	}

	if len(trees) >= 2 {
		// Combine first two trees
		currNode := &BinaryNode{Parent: nil, Left: trees[0].Root, Right: trees[1].Root, Data: nil}
		// Combine the remainting trees, adding the first to the next, then the result of that to the next, etc.
		for i := 2; i < len(trees); i++ {
			tree := trees[i]
			// fmt.Printf("Adding tree: ")
			// PrintPostOrder(tree.Root)

			nextNode := &BinaryNode{Parent: nil, Left: currNode, Right: tree.Root, Data: nil}
			currNode.Parent = nextNode
			currNode = nextNode
		}
		return &Tree{Root: currNode}
	} else if len(trees) == 1 {
		return trees[0]
	} else {
		return nil
	}
}
