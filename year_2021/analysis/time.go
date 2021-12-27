package main

import (
	"bytes"
	"fmt"
	"log"
	"os"
	"os/exec"
	"strings"
	"time"

	"gonum.org/v1/plot"
	"gonum.org/v1/plot/plotter"
	"gonum.org/v1/plot/plotutil"
	"gonum.org/v1/plot/vg"
)

func TimePart(partPath, inputPath string) time.Duration {
	start := time.Now()

	cmd := exec.Command("go", "run", partPath, inputPath)
	// cmd.Stdin = strings.NewReader("some input")
	var out bytes.Buffer
	cmd.Stdout = &out
	err := cmd.Run()
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("%q\n", out.String())

	elapsed := time.Since(start)
	return elapsed
}

func Chart(dayLabels []string, part1Times []float64, part2Times []float64) {
	groupA := plotter.Values(part1Times)
	groupB := plotter.Values(part2Times)

	p := plot.New()

	p.Title.Text = "Advent of Code 2021 Daily Runtimes"
	p.Y.Label.Text = "Time (ms)"

	w := vg.Points(20)

	barsA, err := plotter.NewBarChart(groupA, w)
	if err != nil {
		panic(err)
	}
	barsA.LineStyle.Width = vg.Length(0)
	barsA.Color = plotutil.Color(1)
	barsA.Offset = -w

	barsB, err := plotter.NewBarChart(groupB, w)
	if err != nil {
		panic(err)
	}
	barsB.LineStyle.Width = vg.Length(0)
	barsB.Color = plotutil.Color(2)

	p.Add(barsA, barsB)
	p.Legend.Add("Part 1", barsA)
	p.Legend.Add("Part 2", barsB)
	p.Legend.Top = true
	p.Legend.TextStyle.Font.Size = 8
	p.Legend.YOffs = 10

	p.NominalX(dayLabels...)

	if err := p.Save(5*vg.Inch, 3*vg.Inch, "barchart.png"); err != nil {
		panic(err)
	}
}

func main() {

	basePath, err := os.Getwd()
	if err != nil {
		log.Println(err)
	}
	basePath = strings.TrimSuffix(basePath, "analysis")
	// fmt.Println(basePath)

	days := 7

	var dayLabels []string
	var part1Times []float64
	var part2Times []float64
	for i := 1; i <= days; i++ {
		dayPath := fmt.Sprintf("%v/day_%02d", basePath, i)
		// fmt.Println(dayPath)
		part1Path := fmt.Sprintf("%v/part1/part1.go", dayPath)
		part2Path := fmt.Sprintf("%v/part2/part2.go", dayPath)
		inputPath := fmt.Sprintf("%v/input.txt", dayPath)

		// Run part1
		part1Time := TimePart(part1Path, inputPath)
		part2Time := TimePart(part2Path, inputPath)

		dayLabels = append(dayLabels, fmt.Sprintf("%02d", i))
		part1Times = append(part1Times, float64(part1Time.Milliseconds()))
		part2Times = append(part2Times, float64(part2Time.Milliseconds()))

		fmt.Printf("Day %02d part1: %v, part2: %v\n\n", i, part1Time, part2Time)
	}
	Chart(dayLabels, part1Times, part2Times)

}
