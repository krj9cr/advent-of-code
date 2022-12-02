package aoc

import scala.io.Source

object Day1 {

  def main(args: Array[String]): Unit = {
    val t0: Long = System.nanoTime()
    val source: Source = Source.fromFile(s"$inputPrefix/day1.txt")
    val input = source.getLines().mkString("\n")

    println(input)
    println(part2(input))

    println("Elapsed time: " + (System.nanoTime() - t0) / 1000000 + " ms")
    source.close()
  }

  def part1(lines: String): Int = {
    val l = lines.split("\n\n")
    l.map(i => {
      println("group\n" + i )
      val sum = i.split("\n").map(s => s.toInt).sum
      println(s"sum: $sum")
      sum
    }).max
  }

  def part2(lines: String): Int = {
    val l = lines.split("\n\n")
    l.map(i => {
      println("group\n" + i)
      val sum = i.split("\n").map(s => s.toInt).sum
      println(s"sum: $sum")
      sum
    }).sorted.takeRight(3).sum
  }
}
