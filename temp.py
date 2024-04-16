import random

data = [
    {"HP": 100},
    {"ATK": 100},
    {"HP": 26.68, "ATK": 26.66, "DEF": 26.66, "ER": 10, "EM": 10},
    {"HP": 19.25, "ATK": 19.25, "DEF": 19, "pDMG": 5, "eDMG": 5, "cDMG": 5, "hDMG": 5, "dDMG": 5, "aDMG": 5, "gDMG": 5, "physDMG": 5, "EM": 2.5},
    {"HP": 22, "ATK": 22, "DEF": 22, "CR": 10, "CD": 10, "HB": 10, "EM": 4}
]

odds = 1.061032864

for item in data:
    for key, value in item.items():
        item[key] = value / 100


print(20/odds)