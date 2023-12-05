import time

class MyMap:
  def __init__(self, dest_range_start, source_range_start, range_len):
    self.dest_range_start = dest_range_start
    self.source_range_start = source_range_start
    self.range_len = range_len

  def __str__(self):
    return str(self.dest_range_start) + ", " + str(self.source_range_start) + ", " + str(self.range_len)

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        #lines = [line.strip() for line in file]
        seeds = []
        maps = []
        curr_map = []
        for line in file:
          line = line.strip()
          if "seeds:" in line:
            s = line.strip("seeds: ")
            s = s.split(" ")
            seeds = [ int(i) for i in s ]
          elif line == "":
            continue
          elif "map" in line:
            if len(curr_map) > 0:
              maps.append(curr_map)
            curr_map = []
          else:
            nums = [ int(i) for i in line.split()]
            curr_map.append(MyMap(nums[0], nums[1], nums[2]))
        maps.append(curr_map)
        return seeds, maps

def mapSeed(seed, myMap):
  # see if seed falls in source range
  source_range_end = myMap.source_range_start + myMap.range_len
  if myMap.source_range_start <= seed < source_range_end:
    # get destination value
    offset = seed - myMap.source_range_start
    return myMap.dest_range_start + offset
  else:
    return None


def part1():
    seeds, maps = parseInput(5)
    #print(seeds)
    #for mapSet in maps:
    #  for m in mapSet:
    #    print(m)
    #  print()
    # TEST
    #print(mapSeed(79, MyMap(52, 50, 48)))
    seedAnswers = []
    for seed in seeds:
      mappedSeed = seed
      for mapSet in maps:
        print("new map set")
        mapSetSeedStart = mappedSeed
        # assuming a seed only works for one m?
        for m in mapSet:
          print(mappedSeed, "using", m)
          newMappedSeed = mapSeed(mappedSeed, m)
          print("got", newMappedSeed)
          if newMappedSeed is not None:
            mappedSeed = newMappedSeed
            break
          else:
            mappedSeed = mapSetSeedStart
      
      print(mappedSeed)
      seedAnswers.append(mappedSeed)
    print(seedAnswers)
    print(min(seedAnswers))
        
          

def part2():
    lines = parseInput(5)
    print(lines)

if __name__ == "__main__":
    print("\nPART 1 RESULT")
    start = time.perf_counter()
    part1()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)

    # print("\nPART 2 RESULT")
    # start = time.perf_counter()
    # part2()
    # end = time.perf_counter()
    # print("Time (ms):", (end - start) * 1000)
