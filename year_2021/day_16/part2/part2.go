package main

import (
	"encoding/hex"
	"fmt"
	"os"
	day16 "year_2021/day_16"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Missing param, provide input file path")
		return
	}
	line := day16.ReadInput(os.Args[1])
	fmt.Printf("Input: %v\n", line)

	// Convert hex to binary string
	hexBytes, err := hex.DecodeString(line)
	if err != nil {
		panic(err)
	}
	binary := ""
	for _, n := range hexBytes {
		binary += fmt.Sprintf("%08b", n)
	}

	fmt.Printf("Binary: %v\n", binary)

	_, res, _ := day16.HandlePacket(binary)
	fmt.Printf("result: %v\n", res)
	// fmt.Printf("version sum: %v\n", versionSum)
}
