package day18

import (
	"bufio"
	"fmt"
	"log"
	"math"
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

func (node *BinaryNode) NodeIsPair() bool {
	if node == nil {
		return false
	} else {
		if node.Left != nil && node.Left.Data != nil && node.Right != nil && node.Right.Data != nil {
			return true
		} else {
			return false
		}
	}
}

func (node *BinaryNode) String() string {
	if node.NodeIsNumber() {
		return fmt.Sprintf("%v", *node.Data)
	}
	if node.NodeIsPair() {
		return fmt.Sprintf("[%v, %v]", *node.Left.Data, *node.Right.Data)
	}
	return "branchNode"
}

func (node *BinaryNode) NodeIsNumber() bool {
	if node == nil {
		return false
	} else {
		if node.Data != nil {
			return true
		}
	}
	return false
}

func Magnitude(node *BinaryNode) int {
	result := 0
	if node != nil {
		if node.Left != nil {
			result += 3 * Magnitude(node.Left)
		}
		if node.Right != nil {
			result += 2 * Magnitude(node.Right)
		}
		if node.Data != nil {
			return *node.Data
		}
	}
	return result
}

func CanExplode(adjArr []AdjacencyNode) *BinaryNode {
	for _, a := range adjArr {
		if a.Depth >= 5 {
			fmt.Printf("Depth for: %v, parent: %v\n", a.Node, a.Node.Parent)
			return a.Node.Parent
		}
	}
	return nil
}

func CanSplit(adjArr []AdjacencyNode) *BinaryNode {
	for _, a := range adjArr {
		if *a.Node.Data >= 10 {
			return a.Node
		}
	}
	return nil
}

// Find the index of a node in the adjacency list
func (node *BinaryNode) AdjIndex(adjNodes []AdjacencyNode) int {
	for i, a := range adjNodes {
		if a.Node == node {
			return i
		}
	}
	return -1
}

func (node *BinaryNode) Explode(adjNodes []AdjacencyNode) {
	zero := 0
	if node != nil {
		if !node.NodeIsPair() {
			log.Panicf("trying to explode non-pair node: %v\n", node)
		}
		adjIndex := node.Left.AdjIndex(adjNodes)
		if adjIndex == -1 {
			log.Panicf("could not find node: %v in adj nodes\n", node.Left)
		}
		// Get the node to the left
		if adjIndex-1 >= 0 {
			leftRegular := adjNodes[adjIndex-1]
			fmt.Printf("left reg: %v\n", leftRegular)
			// If any, collapse and add it in the Left
			newLeft := *node.Left.Data + *leftRegular.Node.Data
			leftRegular.Node.Data = &newLeft
		}
		adjIndex = node.Right.AdjIndex(adjNodes)
		if adjIndex == -1 {
			log.Panicf("could not find node: %v in adj nodes\n", node.Right)
		}
		// Get the node to the right
		if adjIndex+1 < len(adjNodes) {
			rightRegular := adjNodes[adjIndex+1]
			fmt.Printf("right reg: %v\n", rightRegular)
			newRight := *node.Right.Data + *rightRegular.Node.Data
			rightRegular.Node.Data = &newRight
		}
		// Remove the children from this node
		node.Left = nil
		node.Right = nil
		node.Data = &zero
	}
}

func (node *BinaryNode) Split() {
	if node.Data == nil {
		fmt.Printf("can't split node\n")
		return
	} else {
		if *node.Data >= 10 {
			half := float64(*node.Data) / 2.0
			newLeft := int(math.Floor(half))
			newRight := int(math.Ceil(half))

			left := &BinaryNode{Parent: node, Left: nil, Right: nil, Data: &newLeft}
			right := &BinaryNode{Parent: node, Left: nil, Right: nil, Data: &newRight}

			node.Left = left
			node.Right = right
			node.Data = nil
		}
	}
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

func ReadInput(path string) []*Tree {
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
	return trees
}

func CombineTrees(trees []*Tree) *Tree {
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

func CombineTwoTrees(a *Tree, b *Tree) *Tree {
	currNode := &BinaryNode{Parent: nil, Left: a.Root, Right: b.Root, Data: nil}
	return &Tree{Root: currNode}
}

type AdjacencyNode struct {
	Node  *BinaryNode
	Depth int
}

func (a AdjacencyNode) String() string {
	return fmt.Sprintf("{node: %v, depth: %v}", a.Node, a.Depth)
}

func (node *BinaryNode) AdjacencyArrayWithDepth(depth int) []AdjacencyNode {
	var result []AdjacencyNode
	if node != nil {
		if node.Left != nil {
			result = append(result, node.Left.AdjacencyArrayWithDepth(depth+1)...)
		}
		if node.Right != nil {
			result = append(result, node.Right.AdjacencyArrayWithDepth(depth+1)...)
		}
		if node.Data != nil {
			result = append(result, AdjacencyNode{node, depth})
		}
	}
	return result
}
