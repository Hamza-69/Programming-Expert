import math

while True:
    nbtm = int(input("Enter the number of teams in the tournament: "))
    if nbtm > 1:
        break 
    else:
        print("The minimum number of teams is 2, try again.")

nms = {}
tmnb = 1
while tmnb <= nbtm:
    nm = input(f"Enter the name for team #{tmnb}: ")
    if len(nm) < 2:
        print("Team names must have at least 2 characters, try again.")
    elif nm.count(" ") > 1:
        print("Team names may have at most 2 words, try again.")
    else:
        nms[nm] = None
        tmnb += 1
nbplmn = len(nms) - 1
while True:
    nbpl = int(input("Enter the number of games played by each team: "))
    if nbpl < nbplmn:
        print("Invalid number of games. Each team plays each other at least once in the regular season, try again.")
    else:
        break

for i in list(nms.keys()):
    while True:
        win = int(input(f"Enter the number of wins Team {i} had: "))
        if win < 0:
            print("The minimum number of wins is 0, try again.")
            continue
        if win > nbpl:
            print(f"The maximum number of wins is {nbpl}, try again.")
            continue
        nms[i] = win 
        break

def sort_win(lst):
    return lst[1]

nms = list(nms.items())
sli = int(len(nms)/2)
nms.sort(reverse=True,key=sort_win)

nmswin = nms[:sli]
nmslose = nms[sli:]
nmswinnew = []
nmslosenew = []
for i in nmswin:
    nmswinnew.append(i[0])
for i in nmslose:
    nmslosenew.append(i[0])

nmswin = nmswinnew
nmslose = nmslosenew[::-1]

for i in range(len(nmswin)):
    print(f"Home: {nmslose[i]} VS Away: {nmswin[i]}")
