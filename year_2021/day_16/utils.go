package day16

import (
	"bufio"
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
		binary, result, versionSum := HandleOperator(binary, t)
		return binary, result, version + versionSum
	}
}

func EvalOperator(op int, literals []int) int {
	if op == 0 { // sum
		sum := 0
		for _, l := range literals {
			sum += l
		}
		return sum
	} else if op == 1 { // product
		prod := 1
		for _, l := range literals {
			prod *= l
		}
		return prod
	} else if op == 2 { // min
		min := 999999999
		for _, l := range literals {
			if l < min {
				min = l
			}
		}
		return min
	} else if op == 3 { // max
		max := -9999999
		for _, l := range literals {
			if l > max {
				max = l
			}
		}
		return max
	} else if op == 4 {
		log.Panicf("trying to evaluate literal\n")
	} else if op == 5 { // greater than
		if len(literals) != 2 {
			log.Panicf("greater than op is missing sub packets\n")
		}
		a := literals[0]
		b := literals[1]
		if a > b {
			return 1
		}
		return 0
	} else if op == 6 { // less than
		if len(literals) != 2 {
			log.Panicf("less than op is missing sub packets\n")
		}
		a := literals[0]
		b := literals[1]
		if a < b {
			return 1
		}
		return 0
	} else if op == 7 { // equal
		if len(literals) != 2 {
			log.Panicf("equals op is missing sub packets\n")
		}
		a := literals[0]
		b := literals[1]
		if a == b {
			return 1
		}
		return 0
	} else {
		log.Panicf("unknown op: %v", op)
	}
	return 0
}

// return: binary, res, version
func HandleOperator(binary string, op int) (string, int, int) {
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
		// fmt.Printf("15-bit literals: %v\n", literals)
		return binary, EvalOperator(op, literals), versionSum
	} else if lengthTypeId == '1' { //  11 bit mode
		binary, numSubPackets := GetBits(binary, 11)
		var literals []int
		versionSum := 0
		for i := 0; i < numSubPackets; i++ {
			b, literal, version := HandlePacket(binary)
			binary = b
			versionSum += version
			literals = append(literals, literal)
		}
		// fmt.Printf("11-bit literals: %v\n", literals)
		return binary, EvalOperator(op, literals), versionSum
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
		// fmt.Printf("Next five: %v\n", five)
		numBinary += five[1:]
		if five[0] == '1' {
			continue
		} else { // last packet
			break
		}
	}
	return binary, BinaryStringToInt(numBinary)
}
