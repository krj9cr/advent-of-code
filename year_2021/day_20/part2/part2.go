package main

import (
	"fmt"
	"os"
	day20 "year_2021/day_20"
	"year_2021/utils"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	enhancement, image := day20.ReadInput(os.Args[1])
	fmt.Printf("Enhancement: \n%v\n\nImage:\n", enhancement)
	utils.PrintStringSlice(image)

	steps := 50

	// For num steps
	for step := 0; step < steps; step++ {
		fmt.Printf("Step: %v\n", step)
		// Get assumed empty char, since the infinite image area
		// osciallates between black and white pixels based on the enhance algorithm
		empty := "."
		if step%2 == 0 {
			empty = "."
		} else {
			empty = "#"
		}
		// Use this for the example
		// if step%2 == 0 { // even
		// 	if enhancement[0] == '.' {
		// 		empty = "."
		// 	} else {
		// 		empty = "#"
		// 	}
		// } else { //odd
		// 	if enhancement[len(enhancement)-1] == '#' {
		// 		empty = "."
		// 	} else {
		// 		empty = "#"
		// 	}
		// }
		// if step == 0 {
		// 	empty = "."
		// }

		// Add 2 rows padding around image
		image2 := day20.PadImage(image, 1, empty)
		image = image2
		utils.PrintStringSlice(image)
		fmt.Print("\n")

		// Make a copy of image for us to update and simultaneously consider pixels
		var imageCopy []string
		// For each pixel (not considering outer most padding?)
		for j := 0; j < len(image); j++ {
			row := []byte(image[j])

			for i := 0; i < len(row); i++ {
				// Get the 9 pixels around it, convert them to binary, then decimal
				newPixel := day20.GetNewPixel(enhancement, image, i, j, empty)
				// Get the pixel from enhancement and set the center pixel
				row[i] = newPixel
			}
			imageCopy = append(imageCopy, string(row))
		}
		// utils.PrintStringSlice(image)
		image = imageCopy
		utils.PrintStringSlice(image)
		fmt.Print("\n")
	}

	count := day20.NumLitPixels(image)
	fmt.Printf("Result: %v\n", count)
}
