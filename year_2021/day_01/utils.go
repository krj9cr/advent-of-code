package day01

func CountIncreasing(lines []int) int {
	var count int = 0
	var size = len(lines)
	for i, l := range lines {
		if i+1 < size {
			var next = lines[i+1]
			if next > l {
				count += 1
			}
		}
	}
	return count
}
