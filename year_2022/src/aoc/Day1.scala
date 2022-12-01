package aoc

import scala.io.Source

object Day1 {

  def main(args: Array[String]): Unit = {
    val t0: Long = System.nanoTime()
    val source: Source = Source.fromFile(s"$inputPrefix/day1.txt")
    val input = source.getLines().map(_.toInt)

    println(part1(input))

    println("Elapsed time: " + (System.nanoTime() - t0) / 1000000 + " ms")
    source.close()
  }

  def part1(lines: Iterator[Int]): Int =
    lines
      .sliding(2)
      .count { case Seq(a, b) => b > a }

  def part2(lines: Iterator[Int]): Int =
    lines
      .sliding(3)
      .map(a => a.sum)
      .sliding(2)
      .count { case Seq(a, b) => b > a }
}
