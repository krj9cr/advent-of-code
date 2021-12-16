package day16

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

func ReadInput(path string) string {
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

	return lines[0]
}

func BinaryStringToInt(binary string) int {
	intval, err := strconv.ParseInt(binary, 2, 64)
	if err != nil {
		panic(err)
	}
	return int(intval)
}

func GetBits(binary string, numBits int) (string, int) {
	typeBits := binary[0:numBits]
	return binary[numBits:], BinaryStringToInt(typeBits)
}

func GetVersionAndType(binary string) (string, int, int) {
	binary, version := GetBits(binary, 3)
	binary, t := GetBits(binary, 3)
	return binary, version, t
}

// returns: binary, result, version
func HandlePacket(binary string) (string, int, int) {
	binary, version, t := GetVersionAndType(binary)
	if t == 4 {
		binary, literal := HandleLiteral(binary)
		return binary, literal, version
	} else {
		binary, result, versionSum := HandleOperator(binary)
		return binary, result, version + versionSum
	}
}

// return: binary, res, version
func HandleOperator(binary string) (string, int, int) {
	lengthTypeId := binary[0]
	binary = binary[1:]
	if lengthTypeId == '0' { // 15 bit mode
		binary, totalLengthBits := GetBits(binary, 15)
		subPackets := binary[:totalLengthBits]
		binary = binary[totalLengthBits:]
		var literals []int
		versionSum := 0
		for {
			if len(subPackets) > 0 {
				sp, literal, version := HandlePacket(subPackets)
				versionSum += version
				literals = append(literals, literal)
				subPackets = sp
			} else {
				break
			}
		}
		// TODO Some operation over literals?
		fmt.Printf("15-bit literals: %v\n", literals)
		return binary, 0, versionSum
	} else if lengthTypeId == '1' { //  11 bit mode

	} else {
		log.Panicf("unknown lengthTypeId %v\n", lengthTypeId)
	}
	return binary, 0, 0
}

func HandleLiteral(binary string) (string, int) {
	numBinary := ""
	// Parse groups of packets until one starts with '0'
	for {
		// Get next 5
		five := binary[0:5]
		binary = binary[5:]
		fmt.Printf("Next five: %v\n", five)
		numBinary += five[1:]
		if five[0] == '1' {
			continue
		} else { // last packet
			break
		}
	}
	return binary, BinaryStringToInt(numBinary)
}
