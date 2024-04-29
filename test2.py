goal_artifacts = []
amount = None
while True:
    amount = input("How many artifacts do you want to generate? Input \'set\' to generate an entire set: ")
    if amount == "set":
        break
    try:
        amount = int(amount)
        if amount > 0:
            break
    except ValueError:
        print("Please enter a number greater than 1 or \'set\'.")
        continue
    if amount < 1:
        print("Please enter a number greater than 1 or \'set\'.")


print(amount)