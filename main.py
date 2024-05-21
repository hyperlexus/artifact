# hooray, no external libraries needed for the entire code
import copy
import math
import random
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
# other stuff
double_5star = 0.061032864

# possible running modes
modes = [
    "Mode 0: generate X random artifacts",
    "Mode 1: simulate X domain runs",
    "Mode 2: generate artifacts until X certain correct artifacts come out",
    "Mode 3: generate artifacts until the correct artifact with all correct substats comes out",
    "Mode 4: generate artifacts until the correct artifact with all correct substats and all correct rolls comes out",
    "Mode 5: input or generate an artifact and roll its substats manually"
]


# helpers (yes i know these are unreadable, i didnt want them to be endlessly long since they're just one-time functionality)
def notin(x, y):
    # returns true if an array 'x' is not in 2d array 'y'
    return not any(all(xe == ye for xe, ye in zip(x, sa)) for sa in y)


def i2d(x, y):
    # returns index of array x in 2d array y; "index 2d"
    for i, r in enumerate(y):
        if all(e == v for e, v in zip(x, r)):
            return i
    return -1


def rin(n, x):
    # returns float s, rounded only if float 'n' has int 'x' or more decimals; "round if necessary"
    s = f"{{:.{x}f}}".format(n)
    return float(s)


def am(s, a):
    # returns index of element s in array a; "array matcher"
    for i in range(len(a)):
        if s == a[i]:
            return i


def cia(a1, a2, n):
    # returns whether int n elements of array a1 match elements in array a2; "contained in array"
    return len(set(a1) & set(a2)) >= n


def ca3(a, b, n):
    # returns whether int 'n' elements of 2d arrays inside array 'a' match a 2d array in the same spot in array 'b'; "compare array 3" (for mode 3)
    c = 0
    for i in range(len(b)):
        if type(b[i]) == list:
            for j in a[3]:
                if j in b[3]:
                    c += 1
            return c >= n
        else:
            if b[i] != a[i]:
                return False
    return True


def cso(di):
    # calculates odds of getting all substats in list 'di' out of the dictionary.
    d = {"HP": 6, "ATK": 6, "DEF": 6, "%HP": 4, "%ATK": 4, "%DEF": 4, "ER": 4, "EM": 4, "CR": 4, "CD": 4}
    tw, pr = sum(d.values()), 1.0
    for i in di:
        if i in d:
            iw = d[i]
            pr *= iw / tw
            tw -= iw
            del d[i]
    return pr


def new_mainstat_artifact():
    # generates a new artifact in the format of [x, y, z] with x = on-set/off-set, y = type of artifact and z = main-stat.
    odds = []
    results = []
    for j in range(3):
        odds.append(random.random())

    # on-set or off-set. 0=onset 1=offset
    results.append(round(odds[0]))
    # what piece, check artifact_list
    results.append(math.floor(odds[1] * 5)) if odds[1] < 0.99999 else results.append(4)
    # main stat, check mainstat_odds
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
    # adds artifact substats to an artifact. input artifact [x,y,z], output artifact [x, y, z, [a, b, c, d, n]] where a-d are substats and n is whether the artifact rolled 3 or 4 stats. mode controls odds for 4 stats
    randomnumber = random.random()
    results = []
    number_stats = 3

    # 3 or 4 substats, domain = 0 and strongbox = 1
    if mode == 0:
        if randomnumber < 0.2:
            number_stats = 4
    elif mode == 1:
        if randomnumber < 0.34:
            number_stats = 4
    else:
        print("im a idiot")
        sys.exit(69420)

    # remove main stat from weight
    sum_substats = 46
    mod_dict = copy.deepcopy(substat_weight)
    item_to_pop = list(mainstat_odds[artifact[1]].items())[artifact[2]]
    if item_to_pop[0] in mod_dict:
        sum_substats -= mod_dict[item_to_pop[0]]
        mod_dict.pop(item_to_pop[0])

    # adds random substats based on main stat and randomnumber
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
    artifact.append(results)
    return artifact

    # append a "-1" as substats[4] if artifact rolls 3 stats only so we know if the artifact was "supposed to" roll 3 or 4 stats.
    # we still need the 4th so we dont have to do calculations twice.


def add_rolls(artifact):
    # takes an artifact as input and returns the same artifact with its rolls attached.
    if not len(artifact) == 4 or not len(artifact[3]) == 5:
        return False
    artifact.append([])
    rolls = 4 if artifact[3][4] == -1 else 5
    for i in range(rolls):
        randomnumber = random.random()
        artifact[4].append(math.floor(randomnumber*4)) if randomnumber < 0.999 else artifact[4].append(3)
    return artifact


def rolling(domain_mode):
    # generates a fully rolled +20 artifact
    artifact = new_mainstat_artifact()
    artifact = add_substats(artifact, domain_mode)
    artifact = add_rolls(artifact)
    return artifact


def domain_run():
    # accurately simulates a domain run with probability for double artifacts. Returns an array with all artifacts (length either 1 or 2).
    result = []
    double_run = False
    rand = random.random()
    result.append(new_mainstat_artifact())
    result[0] = add_substats(result[0], 0)
    if rand < double_5star:
        result.append(new_mainstat_artifact())
        result[1] = add_substats(result[1], 0)
        double_run = True
    return result, double_run


def resin(runs, mode):
    # calculates resin spent for artifacts or domains, and the time it takes to generate said resin.
    os = 'Resin spent: '
    resin_amount = runs * 20 if mode == 1 else round(runs * 18.84956, 2)

    minutes = int(resin_amount * 8)
    days = minutes // 1440
    weeks = days // 7
    years = weeks // 52
    hours = (minutes % 1440) // 60
    remaining_minutes = minutes % 60

    os += f"{str(round(resin_amount))} on {str(runs)} runs. Time to generate resin: "
    os += f"{days}d {hours:02}h {remaining_minutes:02}m."
    if days > 6:
        days = days % 7
        os = os[:-1]
        os += f" / {weeks}w {days:01}d {hours:02}h {remaining_minutes:02}m."
        if weeks > 52:
            weeks = weeks % 52
            os = os[:-1]
            os += f" / {years}y {weeks:02}w {days:01}d {hours:02}h {remaining_minutes:02}m."
    os += " (this is an estimate as it is random if you get 2 artifacts from 1 domain run.)" if mode == 0 else ""
    return os


def howmany():
    while True:
        amount = input("How many artifacts do you want to generate? Input \'set\' to generate an entire set: ")
        if amount == "set":
            break
        try:
            amount = int(amount)
            if amount > 0:
                break
        except ValueError:
            pass
        print("\u001b[31mPlease input an integer greater than 0 or \'set\'.\u001b[0m")
    return amount


def base_output(artifact, mode):
    # base output function with multiple modes (0,3,4). take an artifact in the form of [a, b, c, [d, e, f, (g, -1/-2)]([h, i, j, k])] and turn it into a sentence.
    actual_substats = 3 if len(artifact[3]) == 3 or artifact[3][4] == -1 else 4
    os = f"Your artifact is an {'on-set' if artifact[0] == 0 else 'off-set'} {artifact_list[artifact[1]]} with mainstat {list(mainstat_odds[artifact[1]].items())[artifact[2]][0]}. Its substats are "
    for i in range(actual_substats):
        os += f"{substat_list[artifact[3][i]]}{', ' if i < actual_substats-1 else ''}"
    if mode == 4:
        os += f"{f', {substat_list[artifact[3][3]]} (added)' if actual_substats == 3 else ''}. It rolled into "
        for i in range(len(artifact[4])):
            os += f"{substat_list[artifact[3][artifact[4][i]]]}{', ' if i < len(artifact[4])-1 else ''}"
    os += '.'
    return os


def output_1(artifacts):
    # terminal output for mode 1. takes one or two artifacts and turns it into a sentence, can consider double 5stars from domains.
    os = '\n'
    if len(artifacts) == 1:
        os += base_output(artifacts[0], 0)
        os = f"Your domain returned{os[17:]}"
    elif len(artifacts) == 2:
        os = f"Your \u001b[33mfirst\u001b[0m{base_output(artifacts[0], 0)[4:]}"[:-1]
        os += f". Your \u001b[34msecond\u001b[0m{base_output(artifacts[1], 0)[4:]}"
    return os


def output_2(artifact, tries, odds):
    # terminal output for mode 2. accept an artifact and turn it into a sentence, and additionally tell the user how lucky they got.
    os = f"Your artifact is an {'on-set ' if artifact[0] == 0 else 'off-set '}{artifact_list[artifact[1]]} with mainstat {list(mainstat_odds[artifact[1]].items())[artifact[2]][0]}"
    prob_better = rin((1 - (1 - odds) ** tries) * 100, 4)
    string_better = "\u001b[32m" + str(prob_better) + "\u001b[0m" if prob_better < 50 else "\u001b[31m" + str(prob_better) + "\u001b[0m"  # this is not allowed in f-strings so it has to be this annoying
    os += f". The odds for this artifact are {rin(odds * 100, 4)}%, {'and' if prob_better > 20 else 'but'} you got it in {tries} tries. The probability of a better result is {string_better}%. (smaller number = better, 50% is average)."
    return os

    # not accurate math, fix sometime :)


def output_3(artifact):
    os = base_output(artifact, 3)
    return os
    # this will be expanded upon later, when i can be bothered to figure out the probabilities


def input_artifact(mode, iteration, entire):
    # takes user input to construct own artifact. Mode 2 is just main stat, Mode 3 is sub-stats and Mode 4 is sub-stats and rolls.

    if mode > 1:
        if iteration > 1:
            print(f"\nYou are now inputting artifact number {iteration + 1}.\n")
        print("\nIt is assumed that you want your artifact to be on-set, so this input step is skipped.") if not entire else ''
        goal_artifact = [0]
        if not entire:
            while True:
                print(f"List of artifact types: {', '.join(artifact_list)}")
                mainstat = (input(f"Input a number from 1 to 5, corresponding with the list above: "))
                try:
                    mainstat = int(mainstat)
                    if 0 < mainstat < 6:
                        goal_artifact.append(mainstat - 1)
                        break
                except ValueError:
                    pass
                print("\u001b[31mPlease input an integer from (inluding) 1 to 5. Try again\u001b[0m\n")
        else:
            goal_artifact.append(iteration)

        if goal_artifact[1] < 0 or goal_artifact[1] > 4:
            return False
        desired_dict = mainstat_odds[goal_artifact[1]]
        if goal_artifact[1] == 0 or goal_artifact[1] == 1:
            print(f"Your artifact is a {artifact_list[goal_artifact[1]]}, and its mainstat can only be {', '.join(desired_dict.keys())}.")
            goal_artifact.append(0)
        else:
            while True:
                print(f"List of possible main stats for your artifact: {', '.join(desired_dict.keys())}")
                mainstat_value = input(f"Input a number from 1 to {len(desired_dict.values())}, corresponding with the list above: ")
                try:
                    mainstat_value = int(mainstat_value) - 1
                    if 0 < mainstat_value < len(desired_dict.values()):
                        goal_artifact.append(mainstat_value)
                        break
                except ValueError:
                    pass
                except IndexError:
                    pass
                print(f"\u001b[31mPlease input an integer from 1 to {len(desired_dict.values())}. Try again\u001b[0m\n")

    if mode > 2:
        # substats, also has some mode 5 functionality
        goal_artifact.append([])
        allowed_list = copy.deepcopy(substat_list)
        item_to_pop = list(mainstat_odds[goal_artifact[1]].items())[goal_artifact[2]]
        if item_to_pop[0] in allowed_list:
            allowed_list.pop(am(item_to_pop[0], allowed_list))
        if mode < 5:
            while True:
                amount = input("You are now inputting substats. How many substats do you want to check for? (1 to 4) ")
                try:
                    amount = int(amount)
                    if 0 < amount < 5:
                        break
                except ValueError:
                    pass
                print("\u001b[32mAn artifact only has a minimum of 1, and a maximum of 4 substats. \u001b[31mPlease input an integer from (including) 1 to 4:\u001b[0m ")
        elif mode == 5:
            amount = 4
            print("Please input the four substats that the artifact has. It will be determined later if it generated with 3 or 4 substats.\n")
        for i in range(amount):
            print(f"List of possible substats: {', '.join(allowed_list)}")
            while True:
                desired_substat = input(f"Input a number from 1 to {len(allowed_list)}, corresponding with the list above: ")
                try:
                    desired_substat = int(desired_substat) - 1
                    if -1 < desired_substat < len(allowed_list):
                        break
                except ValueError:
                    pass
                print(f"\u001b[31mPlease input an integer from (including) 1 to {len(allowed_list)}. Try again\u001b[0m ")
            goal_artifact[3].append(am(allowed_list[desired_substat], substat_list))
            allowed_list.pop(desired_substat)
        if mode == 5:
            if input("Has the artifact rolled 4 substats when it was generated? (Y/n) ") == "n":
                goal_artifact[3].append(-1)
            else:
                goal_artifact[3].append(-2)
    return goal_artifact

def mode0():
    artifacts = []
    while True:
        domain_mode = input('Input chance for 4 substats. domain = 20%, strongbox = 34%. (0 = domain, 1 = strongbox): ')
        try:
            domain_mode = int(domain_mode)
            if domain_mode == 0 or domain_mode == 1:
                break
        except ValueError:
            pass
        if not domain_mode == 0 or domain_mode == 1:
            print("\u001b[31mPlease enter only '0' or '1'.\u001b[0m")
    while True:
        x = input("How many artifacts do you want to generate? ")
        try:
            x = int(x)
            if x > 0:
                break
        except ValueError:
            pass
        print("\u001b[31mPlease input an integer greater than 0.\u001b[0m")
    if x == "set":
        x = 5
    roll = True if input("Do you want to roll your artifact(s) after generating it? (Y/n) ") != "n" else False
    for i in range(x):
        artifacts.append(new_mainstat_artifact())
        artifacts[i] = add_substats(artifacts[i], domain_mode)
        print(base_output(artifacts[i], 0))
    print("\n" + resin(x, domain_mode)) if domain_mode == 0 else print(f"Artifacts consumed in the strongbox: {x * 3} for {x} new artifacts.")
def mode1():
    double_runs = 0
    while True:
        x = input("How many domain runs do you want to simulate? ")
        try:
            if "resin" in x:
                x = int(int(x[:-6]) / 20)
            else:
                x = int(x)
            if x > 0:
                break
        except ValueError:
            pass
        print("\u001b[31mPlease enter an integer greater than 0.\u001b[0m")
    for i in range(x):
        tuplo = domain_run()  # wtf duplo reference
        print(output_1(tuplo[0]))
        if tuplo[1]:
            double_runs += 1
    print("\n" + resin(x, 1))
    print(f"Artifacts generated: {x + double_runs}. This is {x * 20 / (x + double_runs):.5f} resin per artifact."
          f"Note that this number becomes more accurate the more domain runs you do; it converges to 18.84956 Resin with n → ∞")
def mode2():
    goal_artifacts = []
    x, entire = None, False
    x = howmany()
    if x == "set":
        x = 5
        entire = True
    for i in range(x):
        goal_artifacts.append(input_artifact(2, i, entire))
        while not goal_artifacts[i]:
            print("\n\u001b[31mYou seem to have made a mistake in the artifact inputting process, "
                  "please read the instructions closely and try again.\u001b[0m")
            goal_artifacts.pop()
            goal_artifacts.append(input_artifact(2, i, entire))
    index, index_pa = 0, 1
    tries = []
    print('')
    artifact = new_mainstat_artifact()
    while len(goal_artifacts) > 0:
        if notin(artifact, goal_artifacts):
            artifact = new_mainstat_artifact()
            index_pa += 1
        else:
            pop_index = i2d(artifact, goal_artifacts)
            odds = round(0.5 * 0.2 * [value for value in mainstat_odds[goal_artifacts[pop_index][1]].values()][goal_artifacts[pop_index][2]], 5)
            index += index_pa
            tries.append(index_pa)
            index_pa = 0
            print(f"{output_2(goal_artifacts[pop_index], index, odds)}")
            goal_artifacts.pop(pop_index)
    print(f"\nThe entire process took {index} tries. Tries per artifact: {', '.join([str(i) for i in tries])}")
    print(resin(index, 0))
def mode3():
    goal_artifacts, tries, found = [], [], []
    x, entire = howmany(), False
    while True:
        domain_mode = input('input chance for 4 substats. domain = 20%, strongbox = 34%. (0 = domain, 1 = strongbox): ')
        try:
            domain_mode = int(domain_mode)
            if domain_mode == 0 or domain_mode == 1:
                break
        except ValueError:
            pass
        print("\u001b[31mPlease enter only '0' or '1'.\u001b[0m")
    if x == "set":
        x = 5
        entire = True
    for i in range(x):
        goal_artifacts.append(input_artifact(3, i, entire))
        while not goal_artifacts[i]:
            print("\n\u001b[31mYou seem to have made a mistake in the artifact inputting process, "
                  "please read the instructions closely and try again.\u001b[0m")
            goal_artifacts.pop()
            goal_artifacts.append(input_artifact(3, i, entire))
    index, index_pa = 0, 1
    print('')
    artifact = new_mainstat_artifact()
    artifact = add_substats(artifact, domain_mode)
    using_artifact = copy.deepcopy(artifact)
    using_artifact[3] = using_artifact[3][:-2] if using_artifact[3][4] == -1 else using_artifact[3][:-1]
    while len(goal_artifacts) > 0:
        for j in range(len(goal_artifacts)):
            if len(found) > 1:
                break
            if ca3(using_artifact, goal_artifacts[j], len(goal_artifacts[j][3])):
                found.append(goal_artifacts[am(goal_artifacts[j], goal_artifacts)])
                break
            else:
                index_pa += 1
                artifact = new_mainstat_artifact()
                artifact = add_substats(artifact, domain_mode)
                using_artifact = copy.deepcopy(artifact)
                using_artifact[3] = using_artifact[3][:-2] if using_artifact[3][4] == -1 else using_artifact[3][:-1]
        while len(found) > 0:
            goal_artifacts.pop(am(found[0], goal_artifacts))
            found.pop(0)
            index += index_pa
            tries.append(index_pa)
            print(output_3(artifact))
            break
    print(f"\nThe entire process took {index} tries. Tries per artifact: {', '.join([str(i) for i in tries])}")
    print(resin(index, 0))
def mode4():
    print(base_output(rolling(0), 4))
def mode5():
    switch = input("Do you want to input the artifact to roll? (Y/n) ")
    while True:
        domain_mode = input('Input chance for 4 substats. domain = 20%, strongbox = 34%. (0 = domain, 1 = strongbox): ')
        try:
            domain_mode = int(domain_mode)
            if domain_mode == 0 or domain_mode == 1:
                break
        except ValueError:
            pass
        if not domain_mode == 0 or domain_mode == 1:
            print("\u001b[31mPlease enter only '0' or '1'.\u001b[0m")
    if switch == "n":
        artifact = rolling(domain_mode)
    else:
        artifact = add_rolls(input_artifact(5, 0, False))
    print(base_output(artifact, 4))


def main():
    # getting program mode from user
    while True:
        mode = input("Enter mode (enter -1 for a list of modes): ")
        try:
            mode = int(mode)
            if mode == -1:
                print('\n'.join([i for i in modes]))
                continue
            if -1 < mode < 6:
                break
        except ValueError:
            pass
        print("\u001b[31mPlease input an integer from (including) -1 to 5. Try again\u001b[0m")
    print(modes[mode])

    (mode0, mode1, mode2, mode3, mode4, mode5)[mode]() #tuple of functions, index is mode


while True:
    main()
    if input("Do you want to run the script again? (Y/n) ") != "n":
        continue
    break