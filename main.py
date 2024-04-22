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
#careful, this is a global variable, dont mess with this
double_runs = 0

# possible running modes
modes = [
"generate X random artifacts",
"simulate X domain runs",
"generate artifacts until X certain correct artifacts come out",
"generate artifacts until the correct artifact with all correct substats comes out",
"generate artifacts until the correct artifact with all correct substats and all correct rolls comes out"
"input or generate an artifact and roll its substats manually"
]

## helpers
def notin(x, y):
    # returns true if an array 'x' is not in 2d array 'y'
    return not any(all(x_elem == y_elem for x_elem, y_elem in zip(x, sub_array)) for sub_array in y)
def i2d(x, y):
    # returns index of array x in 2d array y; "index 2d"
    for i, row in enumerate(y):
        if all(elem == val for elem, val in zip(x, row)):
            return i
    return -1
def rin(n,x):
    # returns float s, rounded only if float 'n' has int 'x' or more decimals; "round if necessary"
    s = f"{{:.{x}f}}".format(n)
    return float(s)
#
def am(s,a):
    # returns index of element s in array a; "array matcher"
    for i in range(len(a)):
        if s == a[i]:
            return i

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

def domain_run():
    # accurately simulates a domain run with probability for double artifacts.
    result = []
    global double_runs
    rand = random.random()
    result.append(new_mainstat_artifact())
    result[0].append(add_substats(result[0], 0))
    if rand<double_5star:
        result.append(new_mainstat_artifact())
        result[1].append(add_substats(result[1], 0))
        double_runs += 1
    return result

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

def output_0(artifact):
    # terminal output for mode 0. take an artifact in the form of [a, b, c, [d, e, f, g, -1/-2]] and turn it into a sentence.
    os = "Your artifact is an "
    os += "on-set " if artifact[0] == 0 else "off-set "
    os += artifact_list[artifact[1]]
    os += " with mainstat "
    os += list(mainstat_odds[artifact[1]].items())[artifact[2]][0]
    os += ". Its substats are "
    substat_amount = 4 if artifact[3][4] == -2 else 3
    for i in range(substat_amount):
        os += substat_list[artifact[3][i]]
        os += ", " if i < substat_amount-1 else ""
    os += "."
    return os

def output_1(artifacts):
    # terminal output for mode 1. takes one or two artifacts and turns it into a sentence, can consider double 5stars from domains.
    os = '\n'
    if len(artifacts) == 1:
        os += output_0(artifacts[0])
        os = os[17:]
        os = f"Your domain returned{os}"
    elif len(artifacts) == 2:
        os = f"Your first{output_0(artifacts[0])[4:]}"[:-1]
        os += f", and your second{output_0(artifacts[1])[4:]}"
    return os

def output_2(artifact, tries, odds):
    # terminal output for mode 2. accept an artifact and turn it into a sentence, and additionally tell the user how lucky they got.
    os = "Your artifact is an "
    os += "on-set " if artifact[0] == 0 else "off-set "
    os += artifact_list[artifact[1]]
    os += " with mainstat "
    os += list(mainstat_odds[artifact[1]].items())[artifact[2]][0]
    if odds > 0:
        os += f". The chance of this happening is {rin(odds*100,4)}%, {'and' if rin((1-(1-odds)**tries)*100,4) > 80 else 'but'} you got it in {tries} tries. The probability of a better result is {rin((1-(1-odds)**tries)*100,4)}%. (smaller number = better, 50% is average)."
    elif odds == 0:
        os += f"The entire process took a total of {tries} tries."
    return os

def input_artifact(mode, iteration):
    try:
        # takes user input to construct own artifact. Mode 2 is just main stat, Mode 3 is sub-stats and Mode 4 is sub-stats and rolls.
        if mode > 1:
            print(f"\nYou are now inputting artifact number {iteration+1}.")
            print("\nIt is assumed that you want your artifact to be on-set, so this input step is skipped.")
            goal_artifact = [0]
            print(f"List of artifact types: {', '.join(artifact_list)}")
            goal_artifact.append(int(input(f"Input a number from 1 to 5, corresponding with the list above: "))-1)
            if goal_artifact[1] < 0 or goal_artifact[1] > 4:
                return False
            desired_dict = mainstat_odds[goal_artifact[1]]
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
            amount = int(input("You are now inputting substats. How many substats do you want to check for? "))
            for i in range(amount):
                print(f"List of possible substats: {', '.join(allowed_list)}")
                desired_substat = int(input(f"Input a number from 1 to {len(allowed_list)}, corresponding with the list above: "))-1
                goal_artifact[3].append(am(allowed_list[desired_substat], substat_list))
                allowed_list.pop(desired_substat)
            print(goal_artifact)
    except ValueError:
        return False
    except IndexError:
        return False
    return goal_artifact

def main():
    # getting program mode from user
    while True:
        try:
            mode = int(input("Enter mode: "))
        except:
            print("Please input a number. try again.")
            continue

        if -1<mode<6:
            break
        else:
            print("Enter only integers from (including) 0-5. try again.")
    print(f"Mode {mode}: {modes[mode]}")

    # main execution
    def mode0():
        x = int(input("how many artifacts do you want to create? "))
        artifacts = []
        domain_mode = int(input('input chance for 4 substats. domain = 20%, strongbox = 34%. (0 = domain, 1 = strongbox): '))
        if x < 1:
            print("No artifacts generated. Exiting...")
            sys.exit(69)
        for i in range(x):
            artifacts.append(new_mainstat_artifact())
            artifacts[i].append(add_substats(artifacts[i], domain_mode))
            print(output_0(artifacts[i]))
        if domain_mode == 0 or 1:
            print("\n"+resin(x,domain_mode)) if domain_mode == 0 else print(f"Artifacts consumed in the strongbox: {math.ceil(x/3)} for {x} new artifacts.")
    def mode1():
        x = input("how many domain runs do you want to simulate? ")
        if "resin" in x:
            x = int(int(x[:-6]) / 20)
        else:
            x = int(x)
        artifacts = []
        for i in range(x):
            print(output_1(domain_run()))
        print("\n"+resin(x, 1))
        print(f"Artifacts generated: {x+double_runs}. This is {x*20/(x+double_runs):.5f} resin per artifact. Note that this number becomes more accurate the more domain runs you do; it converges to 18.84956 Resin with n → ∞")
    def mode2():
        goal_artifacts = []
        amount = int(input("How many artifacts do you want to generate? "))
        for i in range(amount):
            goal_artifacts.append(input_artifact(2, i))
            while not goal_artifacts[i]:
                print('')
                print("\u001b[31mYou seem to have made a mistake in the artifact inputting process, please read the instructions closely and try again.\u001b[0m")
                goal_artifacts.pop()
                goal_artifacts.append(input_artifact(2, i))
            artifact = new_mainstat_artifact()
        index, index_pa = 0, 1
        tries = []
        print('')
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
        os = ''
        os += ", ".join([str(i) for i in tries])
        print(f"\nThe entire process took {index} tries. Tries per artifact: {os}")
        print(resin(index, 0))
    def mode3():
        goal_artifacts = []
        amount = int(input("How many artifacts do you want to generate? "))
        for i in range(amount):
            goal_artifacts.append(input_artifact(3, i))
    # why the fuck did python only implement switch statements 3 years ago
    # eval? more like evil
    eval("mode"+str(mode)+"()")

while True:
    try:
        main()
    except NameError:
        print("This mode is not implemented yet (you can help!), or you didn't enter a valid mode. Please hit enter and try again.")
        continue
    except IndexError:
        print("This mode is not implemented yet. Please wait or submit a pull request! <3")
        continue
    if input("Do you want to run the script again? (Y/n)") != "n":
        continue
    else:
        break