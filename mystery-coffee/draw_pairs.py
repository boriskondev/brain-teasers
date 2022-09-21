from datetime import date
import pandas as pd
import random
import json
import os

mystery_coffee_db_file = "mystery_coffee_db.json"
current_month_db_file = input("Name and extension of emails file: ").strip()

current_month_records = pd.read_excel(current_month_db_file, sheet_name=0, skiprows=None)
current_month_emails = current_month_records["Email"].tolist()

additional_email = "filipa.veselinska@doitwise.com"

if len(current_month_emails) % 2 != 0:
    if additional_email not in current_month_emails:
        current_month_emails.append(additional_email)
    else:
        print(f"Email {additional_email} already exists in the DB and the emails are {len(current_month_emails)}.")
        print("Think what should be done and come back again.")
        exit()

current_month_emails = [email.lower() for email in current_month_emails]

current_month, current_year = str(date.today().month), date.today().year
current_month = "0" + current_month if len(current_month) == 1 else current_month

current_month_pairs_file = f"mystery coffee pairs_{current_month}_{current_year}.txt"

if os.path.exists(mystery_coffee_db_file):
    with open(mystery_coffee_db_file) as f:
        mystery_coffee_db = json.load(f)
else:
    mystery_coffee_db = {}

pairs = []

while current_month_emails:
    pair = []

    first_email = random.choice(current_month_emails)

    if first_email not in mystery_coffee_db:
        mystery_coffee_db[first_email] = []

    second_email = random.choice(current_month_emails)

    while second_email is first_email or second_email in mystery_coffee_db[first_email]:
        second_email = random.choice(current_month_emails)

    pair += [first_email, second_email]
    pairs.append(pair)

    mystery_coffee_db[first_email].append(second_email)

    if second_email not in mystery_coffee_db:
        mystery_coffee_db[second_email] = []

    mystery_coffee_db[second_email].append(first_email)

    current_month_emails.remove(first_email)
    current_month_emails.remove(second_email)

if os.path.exists(current_month_pairs_file):
    os.remove(current_month_pairs_file)

with open(current_month_pairs_file, "a+") as file:
    for i in range(len(pairs)):
        file.write(f"Pair {i + 1}: {pairs[i][0]} + {pairs[i][1]}\n")

json_object = json.dumps(mystery_coffee_db, sort_keys=True, indent=4)

with open("mystery_coffee_db.json", "w") as outfile:
    outfile.write(json_object)
