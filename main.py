import random
import math
import sys

artifact_list = ["flower", "feather", "sands", "goblet", "circlet"]
# data from the wiki
mainstat_odds = [
{"HP": 1.0},
{"ATK": 1.0},
{"%HP": 0.2668, "%ATK": 0.2666, "%DEF": 0.2666, "ER": 0.1, "EM": 0.1},
{"%HP": 0.1925, "%ATK": 0.1925, "%DEF": 0.19, "pDMG": 0.05, "eDMG": 0.05, "cDMG": 0.05, "hDMG": 0.05, "dDMG": 0.05, "aDMG": 0.05, "gDMG": 0.05, "physDMG": 0.05, "EM": 0.025},
{"%HP": 0.22, "%ATK": 0.22, "%DEF": 0.22, "CR": 0.1, "CD": 0.1, "HB": 0.1, "EM": 0.04}
]
substat_weight = {"HP": 6, "ATK": 6, "DEF": 6, "%HP": 4, "%ATK": 4, "%DEF": 4, "ER": 4, "EM": 4, "CR": 4, "CD": 4}
substat_list = ["HP", "ATK", "DEF", "%HP", "%ATK", "%DEF", "ER", "EM", "CR", "CD"]
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
    #what piece
    results.append(math.floor(odds[1]*5)) if odds[1]<0.99999 else results.append(4)
    # main stat
    matcher = 0
    index = 0
    for stat, chance in mainstat_odds[results[1]].items():
        matcher += chance
        if matcher >= odds[2]:
            results.append(index)
            break
        index += 1
    return results


def add_substats(artifact, mode):
    randomnumber = random.random()
    results = []
    number_stats = 3

    #3 or 4 substats, domain = 0 and strongbox = 1
    if mode == 0:
        if randomnumber < 0.2:
            number_stats = 4
    elif mode == 1:
        if randomnumber < 0.34:
            number_stats = 4
    else:
        print("im a idiot")
        sys.exit(69420)

    #remove main stat from weight
    sum_substats = 46
    mod_dict = substat_weight
    desired_dict = mainstat_odds[artifact[1]]
    item_to_pop = list(desired_dict.items())[artifact[2]]
    if item_to_pop[0] in mod_dict:
        sum_substats -= mod_dict[item_to_pop[0]]
        mod_dict.pop(item_to_pop[0])

    # literally wtf does this do
    for i in range(4):
        randomstat = random.random() * sum_substats
        matcher = 0
        for substat, chance in mod_dict.items():
            matcher += chance
            if matcher >= randomstat:
                sum_substats -= mod_dict[substat]
                results.append(substat_list.index(substat))
                mod_dict.pop(substat)
                break
    results.append(-1) if number_stats == 3 else results.append(-2)
    return results

# append a "-1" as substats[4] if artifact rolls 3 stats only so we know if the artifact was "supposed to" roll 3 or 4 stats.
# we still need the 4th so we dont have to do calculations twice.

# mode = input("Enter mode: ")

mode = 0 # TEMP FIX REMOVE THIS

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

def output(artifact, mode):
    os = "Your artifact is an "
    os += "on-set " if artifact[0] == 0 else "off-set "
    os += artifact_list[artifact[1]]
    os += " with a "



match mode:
    case 0:
        x = input("how many artifacts do you want to create? ")
        artifact = new_mainstat_artifact()
        artifact.append(add_substats(artifact, int(input('input substat mode (0 = domain, 1 = strongbox): '))))
        print("artifact:", artifact)

        output(artifact, mode)
