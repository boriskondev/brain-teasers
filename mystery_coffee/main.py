import pandas as pd
import random
import json
import os

# TBD:
# What happens when the monthly emails are odd?
# Pairs to be saved in separate file and the results to be formatted
# When testing different iterations at some point the script freezes - investigate why
# To calculate when an infinite loop will begin and what the condition to escape it to be

mystery_coffee_db_file = "mystery_coffee_db.json"

if os.path.exists(mystery_coffee_db_file):
    with open(mystery_coffee_db_file) as json_file:
        mystery_coffee_db = json.load(json_file)
else:
    mystery_coffee_db = {}

current_month_db = "db.xlsx"
current_month_records = pd.read_excel(current_month_db, sheet_name=0, skiprows=None)
current_month_emails = current_month_records["Email"].tolist()

pairs = []

while current_month_emails:
    pair = []
    first_email = random.choice(current_month_emails)

    if first_email not in mystery_coffee_db:
        mystery_coffee_db[first_email] = []

    pair.append(first_email)

    second_email = random.choice(current_month_emails)

    while second_email is first_email or second_email in mystery_coffee_db[first_email]:
        # print(f"in WHILE with e1: {first_email} and e2: {second_email}.")
        # print(f"{len(current_month_emails)} pairs left")
        second_email = random.choice(current_month_emails)

    # print("out")
    pair.append(second_email)
    pairs.append(pair)

    mystery_coffee_db[first_email].append(second_email)

    if second_email not in mystery_coffee_db:
        mystery_coffee_db[second_email] = []

    mystery_coffee_db[second_email].append(first_email)

    # print(f"{len(pairs)} pairs awarded")

    current_month_emails.remove(first_email)
    current_month_emails.remove(second_email)

for i in range(len(pairs)):
    print(f"Pair {i+1}: {pairs[i][0]} and {pairs[i][1]}")

current_month_pairs = f"Current pairs.txt"

with open(current_month_pairs, "a+") as file:
    for i in range(len(pairs)):
        file.write(f"Pair {i + 1}: {pairs[i][0]} and {pairs[i][1]}\n")

json_object = json.dumps(mystery_coffee_db, sort_keys=True, indent=4)

with open("mystery_coffee_db.json", "w") as outfile:
    outfile.write(json_object)