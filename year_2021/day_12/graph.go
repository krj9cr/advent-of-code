package day12

type Graph struct {
	// Vertices describes all vertices contained in the graph
	// The key will be the Key value of the connected vertice
	// with the value being the pointer to it
	Vertices map[string][]string
	// This will decide if it's a directed or undirected graph
	directed bool
}

// We defined constructor functions that create
// new directed or undirected graphs respectively

func NewDirectedGraph() *Graph {
	return &Graph{
		Vertices: map[string][]string{},
		directed: true,
	}
}

func NewUndirectedGraph() *Graph {
	return &Graph{
		Vertices: map[string][]string{},
	}
}

// AddVertex creates a new vertex with the given
// key and adds it to the graph
func (g *Graph) AddVertex(key string) {
	_, ok1 := g.Vertices[key]
	// Check If the vertex already exists
	if !ok1 {
		g.Vertices[key] = []string{}
	}
}

// The AddEdge method adds an edge between two vertices in the graph
func (g *Graph) AddEdge(k1, k2 string) {
	v1, ok1 := g.Vertices[k1]
	v2, ok2 := g.Vertices[k2]

	// Create the vertex if it doesn't exit
	if !ok1 {
		g.AddVertex(k1)
	}
	if !ok2 {
		g.AddVertex(k2)
	}

	// do nothing if the vertices are already connected
	found := false
	for _, v := range v1 {
		if v == k2 {
			found = true
			break
		}
	}
	if !found {
		g.Vertices[k1] = append(v1, k2)
	}

	// If the graph is undirected, add a corresponding
	// edge back from v2 to v1, effectively making the
	// edge between v1 and v2 bidirectional
	if !g.directed && k1 != k2 {
		// Make sure edge doesn't exist already
		found := false
		for _, v := range v2 {
			if v == k1 {
				found = true
				break
			}
		}
		if !found {
			g.Vertices[k2] = append(v2, k1)
		}
		// fmt.Printf("Adding backwards edge from %v to %v\n", v2, v1)
	}

	// fmt.Printf("GRAPH:\n%v\n", g)
}

func (g *Graph) String() string {
	s := ""
	i := 0
	for key, value := range g.Vertices {
		if i != 0 {
			s += "\n"
		}
		s += key + ": "
		for _, v := range value {
			s += v + ", "
		}
		i++
	}
	return s
}

func (g Graph) CountPaths(start string, end string) int {

	// Call util
	return g.countPathsUtil(start, end, []string{start}, 0)
}

func (g Graph) countPathsUtil(curr string, next string, localPath []string, pathCount int) int {
	if curr == next {
		// fmt.Printf("localPaths; %v\n", localPath)
		pathCount++
	} else {
		// fmt.Printf("Recursing with %v: %v\n", curr, g.Vertices[curr])
		for _, v := range g.Vertices[curr] {
			// Check if v is lowercase and already in the path
			if !IsUpper(v) {
				found := false
				for _, p := range localPath {
					if v == p {
						found = true
						break
					}
				}
				if found {
					continue
				}
			}
			// Recurse down this path
			pathCount = g.countPathsUtil(v, next, append(localPath, v), pathCount)

		}
	}

	return pathCount
}

func (g Graph) CountPaths2(start string, end string) int {
	return g.countPathsUtil2(start, end, []string{start}, 0)
}

func (g Graph) countPathsUtil2(curr string, next string, localPath []string, pathCount int) int {
	if curr == next {
		// fmt.Printf("localPaths; %v\n", localPath)
		pathCount++
	} else {
		for _, v := range g.Vertices[curr] {
			// Check if start and end, which should only be in the path ONCE
			if v == "start" {
				continue
			} else if v == "end" {
				found := 0
				for _, p := range localPath {
					if v == p {
						found += 1
					}
				}
				if found >= 1 {
					continue
				}

				// Check if v is lowercase
			} else if !IsUpper(v) {

				// If it's already in the list ONCE, check if any other lowercase is there TWICE
				found := 0
				for _, p := range localPath {
					if p == v {
						found += 1
						break
					}
				}
				// Check if hitmax
				hitMax := false
				if found >= 1 {

					lowerCounts := make(map[string]int, 0)
					for _, p := range localPath {
						if !IsUpper(p) && p != "start" && p != "end" {
							lowerCounts[p] += 1
						}
					}
					// fo
					for _, count := range lowerCounts {
						if count >= 2 {
							hitMax = true
						}
					}
				}
				if hitMax {
					// fmt.Printf("Found %v num time: %v", v, found)
					continue
				}
			}
			// Recurse down this path
			pathCount = g.countPathsUtil2(v, next, append(localPath, v), pathCount)

		}
	}

	return pathCount
}
