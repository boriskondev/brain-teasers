from datetime import datetime
import pandas as pd
import os

# input_file = "first.xlsx"
# output_file_csv = "first_ready.csv"
# output_file_txt = "first_ready.txt"

input_file = "test.xlsx"
output_file_csv = "test_ready.csv"
output_file_txt = "test_ready.txt"

time_start = datetime.now()

entries = pd.read_excel(input_file, sheet_name=0, skiprows=None)

processed_entries = []

for index, row in entries.iterrows():
    id_of_user = row["id"]
    entries_of_user = row["points"]
    if id_of_user % 10000 == 0:
        print("Now on row: " + str(id_of_user))
    for i in range(1, entries_of_user+1):
        processed_entries.append(id_of_user)

print(len(processed_entries))

if os.path.exists(output_file_csv):
    os.remove(output_file_csv)

with open(output_file_csv, "a+") as file:
    for processed_entry in processed_entries:
        file.write(f"{processed_entry}\n")

if os.path.exists(output_file_txt):
    os.remove(output_file_txt)

processed_entries = list(map(lambda x: str(x), processed_entries))

with open(output_file_txt, "w") as file:
    file.write(", ".join(processed_entries))

time_end = datetime.now()
time_took = time_end - time_start

print(f"\nDone! The execution of this script took {time_took.seconds} seconds.")