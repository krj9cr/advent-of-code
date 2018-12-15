# Sum a list of strings that represent ints
def sum_string_ints(lines):
    total = 0
    for line in lines:
        total += int(line)
    return total
