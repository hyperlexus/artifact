import random
import math
import sys

# data from the wiki
artifact_list = ["flower", "feather", "sands", "goblet", "circlet"]
mainstat_odds = [
{"HP": 1.0},
{"ATK": 1.0},
{"%HP": 0.2668, "%ATK": 0.2666, "%DEF": 0.2666, "ER": 0.1, "EM": 0.1},
{"%HP": 0.1925, "%ATK": 0.1925, "%DEF": 0.19, "pDMG": 0.05, "eDMG": 0.05, "cDMG": 0.05, "hDMG": 0.05, "dDMG": 0.05, "aDMG": 0.05, "gDMG": 0.05, "physDMG": 0.05, "EM": 0.025},
{"%HP": 0.22, "%ATK": 0.22, "%DEF": 0.22, "CR": 0.1, "CD": 0.1, "HB": 0.1, "EM": 0.04}
]
substat_weight = {"HP": 6, "ATK": 6, "DEF": 6, "%HP": 4, "%ATK": 4, "%DEF": 4, "ER": 4, "EM": 4, "CR": 4, "CD": 4}
#other stuff
double_5star = 0.061032864

# possible running modes
modes = [
"generate X random artifacts",
"simulate X domain runs",
"generate artifacts until a certain correct artifact comes out",
"generate artifacts until the correct artifact with all correct substats comes out",
"generate artifacts until the correct artifact with all correct substats and all correct rolls comes out"
]

def new_mainstat_artifact():
    odds = []
    results = []
    for j in range(3):
        odds.append(random.random())

    #on-set or off-set
    results.append(round(odds[0]))
    print("on-set") if odds[0] > 0.5 else print("off-set")
    #what piece
    results.append(math.floor(odds[1]*5)) if odds[1]<0.99999 else results.append(4)
    print(artifact_list[results[1]])
    # main stat
    matcher = 0
    index = 0
    for stat, chance in mainstat_odds[results[1]].items():
        matcher += chance
        if matcher >= odds[2]:
            print(stat)
            results.append(index)
            break
        index += 1
    return results

def add_substats(artifact, mode):
    odds = []
    results = []
    four_stats = False
    for j in range(4):
        odds.append(random.random())

    #3 or 4 substats, domain = 0 and strongbox = 1
    if mode == 0:
        if odds[0] < 0.2:
            four_stats = True
    elif mode == 1:
        if odds[0] < 0.34:
            four_stats = True
    else:
        print("im a idiot")
        sys.exit(69420)

    sum_substats = 46
    mod_dict = substat_weight
    mod_dict.pop("%HP")
    print(mainstat_odds[2].items())
    print(mod_dict)

    return results

mode = input("Enter mode: ")
mode_done = False
while not mode_done:
    try:
        mode = int(mode)
    except:
        print("please input a number. try again.")
        mode = input("Enter mode: ")
        continue

    if -1<mode<5:
        mode_done = True
    else:
        print("enter only integers from (including) 0-4. try again.")
        mode = input("Enter mode: ")

print(f"Mode {mode}: {modes[mode]}")

artifact = new_mainstat_artifact()
sub_artifact = add_substats(artifact, int(input('input substat mode: ')))

print("artifact:", artifact)
print("substats:", sub_artifact)

# results:
# on-set, what piece, main stat, sub-stat 1, sub-stat 2, sub-stat 3, sub-stat 4 (if applicable)
