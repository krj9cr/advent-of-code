import main
import part1

# Test part1
test1 = main.get_lines("test1.txt")
test1_actual = part1.sum_string_ints(test1)
test1_expected = 2
print test1_actual
assert test1_actual == test1_expected
