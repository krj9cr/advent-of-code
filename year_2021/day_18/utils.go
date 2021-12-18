package day18

import (
	"bufio"
	"fmt"
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

// Check through a "Tree" if it can explode, return the node that can
func (node *BinaryNode) CanExplode(depth int) *BinaryNode {
	if node == nil {
		return nil
	}
	if depth >= 4 && node.NodeIsPair() {
		return node
	}
	var explode *BinaryNode
	if node.Left != nil {
		explode = node.Left.CanExplode(depth + 1)
		if explode != nil && explode.NodeIsPair() {
			return explode
		}
	}
	if node.Right != nil {
		explode = node.Right.CanExplode(depth + 1)
		if explode != nil && explode.NodeIsPair() {
			return explode
		}
	}
	return nil
}

// Check through a "Tree" if it can split, return the first left node that can
func (node *BinaryNode) CanSplit() *BinaryNode {
	if node == nil {
		return nil
	}
	if node.NodeIsNumber() && *node.Data >= 10 {
		return node
	}
	var left *BinaryNode
	if node.Left != nil {
		left = node.Left.CanSplit()
	}
	if left != nil {
		return left
	} else {
		if node.Right != nil {
			return node.Right.CanSplit()
		}
	}
	return nil
}

func (node *BinaryNode) FindFirstLeaf(left bool, cameFrom *BinaryNode, timesGone int) *BinaryNode {
	if node.Data != nil && timesGone > 0 {
		return node
	}
	if node.Left != nil && node.Left != cameFrom {
		if left {
			timesGone += 1
		}
		return node.Left.FindFirstLeaf(left, node, timesGone)
	}
	if node.Right != nil && node.Left != cameFrom {
		if !left {
			timesGone += 1
		}
		return node.Right.FindFirstLeaf(left, node, timesGone)
	}

	return nil
}

func (node *BinaryNode) FindFirstRegular(left bool, cameFrom *BinaryNode, timesGone int) *BinaryNode {
	if node.Parent != nil {
		goingUpLeft := false
		if node.Parent.Left == node {
			goingUpLeft = false
		}
		if left {
			if node.Parent.Left != nil {
				if node.Parent.Left != node && node.Parent.Left.Data != nil {
					return node.Parent.Left
				}
			}
			if goingUpLeft {
				timesGone += 1
			}
			return node.Parent.FindFirstRegular(left, node, timesGone)
		} else {
			if node.Parent.Right != nil {
				if node.Parent.Right != node && node.Parent.Right.Data != nil {
					return node.Parent.Right
				}
			}
			if !goingUpLeft {
				timesGone += 1
			}
			return node.Parent.FindFirstRegular(left, node, timesGone)
		}
	} else { // start coming back down, unless we just came from that way?
		// timesGone := 0
		if node.Left != cameFrom {
			fmt.Printf("going down left\n")
			if left {
				timesGone += 1
				return node.Left.FindFirstLeaf(left, node, timesGone)
			}
		}
		if node.Right != cameFrom {
			fmt.Printf("going down right\n")
			if !left {
				timesGone += 1
				return node.Right.FindFirstLeaf(left, node, timesGone)
			}
		}
	}
	return nil
}

func (node *BinaryNode) Explode() {
	zero := 0
	if node != nil {
		// Go up the tree, looking for first regular number on the left
		leftRegular := node.FindFirstRegular(true, nil, 0)
		// fmt.Printf("left reg: %v\n", leftRegular)
		// If any, collapse and add it in the Left
		if leftRegular != nil {
			newLeft := *node.Left.Data + *leftRegular.Data
			leftRegular.Data = &newLeft
		}
		// Go up the right tree
		rightRegular := node.FindFirstRegular(false, nil, 0)
		fmt.Printf("right reg: %v\n", rightRegular)
		if rightRegular != nil {
			newRight := *node.Right.Data + *rightRegular.Data
			rightRegular.Data = &newRight
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
