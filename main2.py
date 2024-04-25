# hooray, no external libraries needed for the entire code
import random, math, sys, copy, time

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
    "Mode 0: generate X random artifacts",
    "Mode 1: simulate X domain runs",
    "Mode 2: generate artifacts until X certain correct artifacts come out",
    "Mode 3: generate artifacts until the correct artifact with all correct substats comes out",
    "Mode 4: generate artifacts until the correct artifact with all correct substats and all correct rolls comes out",
    "Mode 5: input or generate an artifact and roll its substats manually"
]

## helpers (yes i know these are unreadable, i didnt want them to be endlessly long since they're just one-time functionality)
def notin(x, y):
    # returns true if an array 'x' is not in 2d array 'y'
    return not any(all(xe == ye for xe, ye in zip(x, sa)) for sa in y)
def i2d(x, y):
    # returns index of array x in 2d array y; "index 2d"
    for i, r in enumerate(y):
        if all(e == v for e, v in zip(x, r)):
            return i
    return -1
def rin(n,x):
    # returns float s, rounded only if float 'n' has int 'x' or more decimals; "round if necessary"
    s = f"{{:.{x}f}}".format(n)
    return float(s)
def am(s,a):
    # returns index of element s in array a; "array matcher"
    for i in range(len(a)):
        if s == a[i]:
            return i
def cia(a1,a2,n):
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
    tw,pr = sum(d.values()),1.0
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

    #on-set or off-set. 0=onset 1=offset
    results.append(round(odds[0]))
    #what piece, check artifact_list
    results.append(math.floor(odds[1]*5)) if odds[1]<0.99999 else results.append(4)
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
    return results

    # append a "-1" as substats[4] if artifact rolls 3 stats only so we know if the artifact was "supposed to" roll 3 or 4 stats.
    # we still need the 4th so we dont have to do calculations twice.

def not_for_rolling(mode):
    artifact = new_mainstat_artifact()
    artifact.append(add_substats(new_mainstat_artifact(), mode))
    artifact[3] = artifact[3][:-2] if artifact[3][4] == -1 else artifact[3][:-1]
    return artifact

def domain_run():
    # accurately simulates a domain run with probability for double artifacts. Returns an array with all artifacts (length either 1 or 2).
    result = []
    double_run = False
    rand = random.random()
    result.append(new_mainstat_artifact())
    result[0].append(add_substats(result[0], 0))
    if rand<double_5star:
        result.append(new_mainstat_artifact())
        result[1].append(add_substats(result[1], 0))
        double_run = True
    return result, double_run

def resin(runs, mode):
    # calculates resin spent for artifacts or domains, and the time it takes to generate said resin.
    os = 'Resin spent: '
    resin_amount = runs*20 if mode == 1 else round(runs*18.84956,2)

    minutes = int(resin_amount*8)
    days = minutes // (24 * 60)
    weeks = days // 7
    years = weeks // 52
    hours = (minutes % (24 * 60)) // 60
    remaining_minutes = minutes % 60

    os += str(round(resin_amount)) + " on " + str(runs) + " runs. Time to generate resin: " if mode == 1 else str(round(resin_amount))+ ". Time to generate resin: "
    os += f"{days}d {hours:02}h {remaining_minutes:02}m."
    if days > 6:
        days = days % 7
        os = os[:-1]
        os += f" / {weeks}w {days:01}d {hours:02}h {remaining_minutes:02}m."
        if weeks > 52:
            weeks = weeks % 52
            os = os[:-1]
            os += f" / {years}y {weeks}w {days:01}d {hours:02}h {remaining_minutes:02}m."
    os += " (this is an estimate as it is random if you get 2 artifacts from 1 domain run.)" if mode == 0 else ""
    return os

def output_0(artifact, mode):
    # terminal output for mode 0 and part of output_3(). take an artifact in the form of [a, b, c, [d, e, f, (g, -1/-2)]] and turn it into a sentence.
    if mode == 0:
        artifact[3] = artifact[3][:-2] if artifact[3][4] == -1 else artifact[3][:-1]
    os = f"Your artifact is an {'on-set' if artifact[0] == 0 else 'off-set'} {artifact_list[artifact[1]]} with mainstat {list(mainstat_odds[artifact[1]].items())[artifact[2]][0]}. Its substats are "
    for i in range(len(artifact[3])):
        os += f"{substat_list[artifact[3][i]]}{', ' if i < len(artifact[3])-1 else ''}"
    os += '.'
    return os, artifact

def output_1(artifacts):
    # terminal output for mode 1. takes one or two artifacts and turns it into a sentence, can consider double 5stars from domains.
    os = '\n'
    if len(artifacts) == 1:
        os += output_0(artifacts[0], 0)
        # os = os[17:]
        os = f"Your domain returned{os[17:]}"
    elif len(artifacts) == 2:
        os = f"Your \u001b[33mfirst\u001b[0m{output_0(artifacts[0], 0)[4:]}"[:-1]
        os += f". Your \u001b[34msecond\u001b[0m{output_0(artifacts[1], 0)[4:]}"
    return os

def output_2(artifact, tries, odds):
    # terminal output for mode 2. accept an artifact and turn it into a sentence, and additionally tell the user how lucky they got.
    os = f"Your artifact is an {'on-set ' if artifact[0] == 0 else 'off-set '}{artifact_list[artifact[1]]} with mainstat {list(mainstat_odds[artifact[1]].items())[artifact[2]][0]}"
    prob_better = rin((1-(1-odds)**tries)*100,4)
    string_better = "\u001b[32m" + str(prob_better) + "\u001b[0m" if prob_better < 50 else "\u001b[31m" + str(prob_better) + "\u001b[0m" # this is not allowed in f-strings so it has to be this annoying
    os += f". The odds for this artifact are {rin(odds*100,4)}%, {'and' if prob_better > 20 else 'but'} you got it in {tries} tries. The probability of a better result is {string_better}%. (smaller number = better, 50% is average)."
    return os

def output_3(artifact):
    str = output_0(artifact, 3)
    return str

def input_artifact(mode, iteration):
    # takes user input to construct own artifact. Mode 2 is just main stat, Mode 3 is sub-stats and Mode 4 is sub-stats and rolls.
    try:

        if mode > 1:
            print(f"\nYou are now inputting artifact number {iteration+1}.")
            print("\nIt is assumed that you want your artifact to be on-set, so this input step is skipped.")
            goal_artifact = [0]
            print(f"List of artifact types: {', '.join(artifact_list)}")
            goal_artifact.append(int(input(f"Input a number from 1 to 5, corresponding with the list above: "))-1)
            if goal_artifact[1] < 0 or goal_artifact[1] > 4:
                return False
            desired_dict = mainstat_odds[goal_artifact[1]]
            if goal_artifact[1] == 0 or goal_artifact[1] == 1:
                print(f"Your artifact is a {artifact_list[goal_artifact[1]]}, and its mainstat can only be {', '.join(desired_dict.keys())}.")
                goal_artifact.append(0)
            else:
                print(f"List of possible main stats for your artifact: {', '.join(desired_dict.keys())}")
                goal_artifact.append(int(input(f"Input a number from 1 to {len(desired_dict.values())}, corresponding with the list above: "))-1)
            if goal_artifact[2] < 0 or goal_artifact[2] > len(desired_dict.values())-1:
                return False

        if mode > 2:
            goal_artifact.append([])
            allowed_list = copy.deepcopy(substat_list)
            item_to_pop = list(mainstat_odds[goal_artifact[1]].items())[goal_artifact[2]]
            if item_to_pop[0] in allowed_list:
                allowed_list.pop(am(item_to_pop[0], allowed_list))
            while True:
                amount = int(input("\nYou are now inputting substats. How many substats do you want to check for? "))
                if 0<amount<5:
                    break
                else:
                    print("An artifact only has a minimum of 1, and a maximum of 4 substats. Please input an integer from 1 to 4.")
                    continue
            for i in range(amount):
                print(f"List of possible substats: {', '.join(allowed_list)}")
                desired_substat = int(input(f"Input a number from 1 to {len(allowed_list)}, corresponding with the list above: "))-1
                goal_artifact[3].append(am(allowed_list[desired_substat], substat_list))
                allowed_list.pop(desired_substat)
    except ValueError:
        return False
    except IndexError:
        return False
    return goal_artifact

def main():
    # getting program mode from user
    while True:
        try:
            mode = int(input("Enter mode (enter -1 for a list of modes): "))
        except:
            print("Please input a number. try again.")
            continue

        if mode == -1:
            print('\n'.join([i for i in modes]))
            continue
        if -2<mode<6:
            break
        else:
            print("Enter only integers from (including) 0-5. try again.")
    print(modes[mode])

    # main execution
    match mode:
        case 0:
            x = int(input("How many artifacts do you want to create? "))
            artifacts = []
            domain_mode = int(input('input chance for 4 substats. domain = 20%, strongbox = 34%. (0 = domain, 1 = strongbox): '))
            for i in range(x):
                artifacts.append(new_mainstat_artifact())
                artifacts[i].append(add_substats(artifacts[i], domain_mode))
                print(output_0(artifacts[i], 0))
            if domain_mode == 0 or 1:
                print("\n"+resin(x,domain_mode)) if domain_mode == 0 else print(f"Artifacts consumed in the strongbox: {math.ceil(x/3)} for {x} new artifacts.")
        case 1:
            double_runs = 0
            x = input("How many domain runs do you want to simulate? ")
            if "resin" in x:
                x = int(int(x[:-6]) / 20)
            else:
                x = int(x)
            artifacts = []
            for i in range(x):
                tuplo = domain_run() # wtf duplo reference
                print(output_1(tuplo[0]))
                if tuplo[1]:
                    double_runs += 1
            print("\n"+resin(x, 1))
            print(f"Artifacts generated: {x+double_runs}. This is {x*20/(x+double_runs):.5f} resin per artifact. Note that this number becomes more accurate the more domain runs you do; it converges to 18.84956 Resin with n → ∞")
        case 2:
            goal_artifacts = []
            amount = int(input("How many artifacts do you want to generate? "))
            for i in range(amount):
                goal_artifacts.append(input_artifact(2, i))
                while not goal_artifacts[i]:
                    print('')
                    print("\u001b[31mYou seem to have made a mistake in the artifact inputting process, please read the instructions closely and try again.\u001b[0m")
                    goal_artifacts.pop()
                    goal_artifacts.append(input_artifact(2, i))
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
        case 3:
            goal_artifacts = []
            amount = int(input("How many artifacts do you want to generate? "))
            domain_mode = int(input('input chance for 4 substats. domain = 20%, strongbox = 34%. (0 = domain, 1 = strongbox): '))
            for i in range(amount):
                goal_artifacts.append(input_artifact(3, i))
                while not goal_artifacts[i]:
                    print("\n\u001b[31mYou seem to have made a mistake in the artifact inputting process, please read the instructions closely and try again.\u001b[0m")
                    goal_artifacts.pop()
                    goal_artifacts.append(input_artifact(3, i))
            index, index_pa = 0, 1
            tries = []
            print('')
            found = []
            artifact = not_for_rolling(domain_mode)
            while len(goal_artifacts) > 0:
                for j in range(len(goal_artifacts)):
                    if len(found) > 1:
                        break
                    if ca3(artifact, goal_artifacts[j], len(goal_artifacts[j][3])):
                        found.append(goal_artifacts[am(goal_artifacts[j], goal_artifacts)])
                        break
                    else:
                        index_pa += 1
                        artifact = not_for_rolling(domain_mode)
                while len(found) > 0:
                    goal_artifacts.pop(am(found[0],goal_artifacts))
                    found.pop(0)
                    index += index_pa
                    tries.append(index_pa)
                    print(output_3(artifact))
                    break
            print(f"\nThe entire process took {index} tries. Tries per artifact: {', '.join([str(i) for i in tries])}")
            print(resin(index, 0))


while True:
    main()

    if input("Do you want to run the script again? (Y/n)") != "n":
        double_runs = 0
        continue
    else:
        break