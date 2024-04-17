import random

results_odds = {"HP": 19.25, "ATK": 19.25, "DEF": 19, "pDMG": 5, "eDMG": 5, "cDMG": 5, "hDMG": 5, "dDMG": 5, "aDMG": 5, "gDMG": 5, "physDMG": 5, "EM": 2.5}

random_pick = random.random() * 100

current_odds = 0
for result, odds in results_odds.items():
    current_odds += odds
    if current_odds >= random_pick:
        print("Selected result:", result, ", number:", random_pick/100)
        break


#print(results_odds.items())

# discord fuckery
handshakes = ""
for i in range(1, 6):
    for j in range(1, 6):
        if i != j:
            handshakes += ":handshake_tone" + str(j) + "_tone" + str(i) + ": "
        else:
            continue
#print(handshakes)

# binomial
def cdf(n,p):
    # Building my own binomial distribution because yuck, libraries
    p1=n*p*(1-p)**(p-1)
    prc=p1*100
    return prc


print(cdf(11, 0.1))
