import random
import math

final_odds = 0
artifacts = ["flower", "feather", "sands", "goblet", "circlet"]
# main stat odds
mainstat_odds = [
{"HP": 1.0},
{"ATK": 1.0},
{"HP": 0.2668, "ATK": 0.2666, "DEF": 0.2666, "ER": 0.1, "EM": 0.1},
{"HP": 0.1925, "ATK": 0.1925, "DEF": 0.19, "pDMG": 0.05, "eDMG": 0.05, "cDMG": 0.05, "hDMG": 0.05, "dDMG": 0.05, "aDMG": 0.05, "gDMG": 0.05, "physDMG": 0.05, "EM": 0.025},
{"HP": 0.22, "ATK": 0.22, "DEF": 0.22, "CR": 0.1, "CD": 0.1, "HB": 0.1, "EM": 0.04}
]

# data from the wiki
double_5star = 0.061032864
domain_four_stats_odds = 0.2
strongbox_four_stats_odds = 0.34 #yes, not rounded

modes = [
"simulate X domain runs",
"generate X random artifacts",
"generate artifacts until a certain correct artifact comes out",
"generate artifacts until the correct artifact with all correct substats comes out",
"generate artifacts until the correct artifact with all correct substats and all correct rolls comes out"
]

def generate_mainstat_artifact():
    odds = []
    results = []
    for j in range(8):
        odds.append(random.random())

    #on-set or off-set
    results.append(round(odds[0]))
    #what piece
    results.append(math.floor(odds[1]*5)) if odds[1]<0.99999 else results.append(4)
    # main stat


    print(odds)
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

print(f"Mode {mode}: " + modes[mode])
print("artifact:" ,generate_mainstat_artifact())


# results:
# on-set, what piece, main stat, sub-stat 1, sub-stat 2, sub-stat 3, sub-stat 4 (if applicable)


# match mode:
#     case 0:


