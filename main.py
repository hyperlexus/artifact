import random

final_odds = 0
artifacts = ["flower", "feather", "sands", "goblet", "circlet"]
# main stat odds
flower_odds = {"HP": 100}
feather_odds = {"ATK": 100}
# all values except EM are in %
sands_odds = {"HP": 26.68, "ATK": 26.66, "DEF": 26.66, "ER": 10, "EM": 10}
goblet_odds = {"HP": 19.25, "ATK": 19.25, "DEF": 19, "pDMG": 5, "eDMG": 5, "cDMG": 5, "hDMG": 5, "dDMG": 5, "aDMG": 5, "gDMG": 5, "physDMG": 5, "EM": 2.5}
circlet_odds = {"HP": 22, "ATK": 22, "DEF": 22, "CR": 10, "CD": 10, "HB": 10, "EM": 4}



# data from the wiki
double_5star = 0.061032864
domain_four_stats_odds = 0.2
strongbox_four_stats_odds = 0.34
set_odds = 0.5
correct_artifact_odds = 0.2

modes = [
"generate one random artifact",
"generate X random artifacts",
"generate artifacts until a certain correct artifact comes out",
"generate artifacts until the correct artifact with all correct substats comes out"
]
def generate_empty_artifact():
    odds = []
    results = []
    for j in range(5):
        odds.append(random.random())
    if double_5star < odds[0]:
        results.append(1)
        double = True
    else:
        results.append(0)
    if double == True:
        artifact2 = []


    return odds, results

mode = input("mode: ")
mode_done = False
while not mode_done:
    try:
        mode = int(mode)
    except:
        print("please input a number. try again.")
        mode = input("mode: ")
        continue

    if -1<mode<4:
        mode_done = True
    else:
        print("enter either 0,1,2,3. try again.")
        mode = input("mode: ")

print(f"Mode {mode}: " + modes[mode])
print(generate_empty_artifact())

# match mode:
#     case 0:


