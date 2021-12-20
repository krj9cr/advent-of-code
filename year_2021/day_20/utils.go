package day20

import (
	"bufio"
	"log"
	"os"
	"strconv"
	"strings"
)

func NumLitPixels(image []string) int {
	count := 0
	for _, row := range image {
		for _, item := range row {
			if item == '#' {
				count += 1
			}
		}
	}
	return count
}

func GetNewPixel(enhancement string, image []string, i int, j int, empty string) byte {
	index := Get3x3IntVal(image, i, j, empty)
	newPixel := enhancement[index]
	// fmt.Printf(" newPixel: %v\n", newPixel)
	return newPixel
}

func Get3x3IntVal(image []string, i int, j int, empty string) int {
	pixelString := Get3x3String(image, i, j, empty)
	binaryString := PixelStringToBinaryString(pixelString)
	intval, err := strconv.ParseInt(binaryString, 2, 64)
	// fmt.Printf("pixel: %v at (%v, %v)\n pixelSTring: %v\n binaryString: %v\n intval: %v\n", string(image[j][i]), i, j, pixelString, binaryString, intval)
	if err != nil {
		panic(err)
	}
	return int(intval)
}

func Get3x3String(image []string, i int, j int, empty string) string {
	firstRow := ""
	if j-1 >= 0 {
		if i-1 >= 0 {
			firstRow += string(image[j-1][i-1])
		} else {
			firstRow += empty
		}
		firstRow += string(image[j-1][i])
		if i+1 < len(image[0]) {
			firstRow += string(image[j-1][i+1])
		} else {
			firstRow += empty
		}
	} else {
		firstRow = strings.Repeat(empty, 3)
	}

	secondRow := ""
	if i-1 >= 0 {
		secondRow += string(image[j][i-1])
	} else {
		secondRow += empty
	}
	secondRow += string(image[j][i])
	if i+1 < len(image[0]) {
		secondRow += string(image[j][i+1])
	} else {
		secondRow += empty
	}

	thirdRow := ""
	if j+1 < len(image) {
		if i-1 >= 0 {
			thirdRow += string(image[j+1][i-1])
		} else {
			thirdRow += empty
		}
		thirdRow += string(image[j+1][i])
		if i+1 < len(image[0]) {
			thirdRow += string(image[j+1][i+1])
		} else {
			thirdRow += empty
		}
	} else {
		thirdRow = strings.Repeat(empty, 3)
	}
	return firstRow + secondRow + thirdRow
	// Assume we stay in bounds because of padding
	// return string(image[j-1][i-1]) + string(image[j-1][i]) + string(image[j-1][i+1]) +
	// string(image[j][i-1]) + string(image[j][i]) + string(image[j][i+1]) +
	// string(image[j+1][i-1]) + string(image[j+1][i]) + string(image[j+1][i+1])
}

func PixelStringToBinaryString(pixels string) string {
	result := ""
	for _, c := range pixels {
		if c == '.' {
			result += "0"
		} else if c == '#' {
			result += "1"
		} else {
			log.Panicf("unknown pixel: %v\n", c)
		}
	}
	return result
}

func PadImage(image []string, times int, char string) []string {
	w := len(image[0])

	// Make top rows
	var topRows []string
	for t := 0; t < times; t++ {
		topRows = append(topRows, strings.Repeat(char, w))
	}
	// Make bottom rows
	bottomRows := make([]string, len(topRows))
	copy(bottomRows, topRows)

	// Join rows
	image2 := append(append(topRows, image...), bottomRows...)

	// Add columns
	var result []string
	colPad := strings.Repeat(char, times)
	for _, row := range image2 {
		result = append(result, colPad+row+colPad)
	}

	return result
}

func ReadInput(path string) (string, []string) {
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

	if len(lines) < 1 {
		log.Panicf("could not read input\n")
	}
	enhancement := lines[0]

	image := lines[2:]

	return enhancement, image
}
