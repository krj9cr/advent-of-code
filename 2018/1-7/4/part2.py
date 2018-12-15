import sys
from datetime import datetime

if len(sys.argv) < 2:
    print "Usage: " + sys.argv[0] + " <input>"
    exit(1)

input = sys.argv[1]

# map of guard ids to list of sleeping events for that guard
events = []
# read input
with open(input, 'r') as file:
    for line in file:
        split = line.strip().split("]")
        # make a [ datetime, string ]
        dt = datetime.strptime(split[0].strip("["), '%Y-%m-%d %H:%M')
        s = split[1].strip()
        events.append([dt, s])

# sort events by datetime
events = sorted(events, key=lambda x: x[0])

# print events
# for line in events:
#     print line

# group events by guard id
guard_events = {}
id = "?"
for event in events:
    action = event[1]
    if "Guard" in action:
        id = int(action.split(" ")[1].strip("#"))
        # print id
        if guard_events.get(id) is None:
            guard_events[id] = []
    else:
        list = guard_events[id]
        list.append(event)

# print guard_events

# find the most minute for each guard
guard_sleeps = {}
guard_most = {}
for id in guard_events:
    gevents = guard_events.get(id)
    guard_minutes = {}
    for i in range(0, 60):
        guard_minutes[i] = 0
    # get time delta between each pair of events
    for i in range(0, len(gevents) - 1, 2):
        dtg1 = gevents[i + 1][0]
        dtg2 = gevents[i][0]
        delta = dtg1 - dtg2
        minutes = delta.seconds // 60
        for i in range(0, minutes):
            guard_minutes[dtg2.minute+i] += 1
        # print dtg2.minute, dtg1.minute, minutes
    # print guard_minutes
    most_minute = max(guard_minutes, key=lambda x: guard_minutes[x])
    guard_most[id] = [most_minute, guard_minutes[most_minute]]

mostest_guard = max(guard_most, key=lambda x: guard_most[x][1])
mostest_minute = guard_most[mostest_guard][0]

# print guard_most

print str(mostest_guard) + " * " + str(mostest_minute) + " = " + str(mostest_guard * mostest_minute)
