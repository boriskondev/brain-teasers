# import OS module
import os

# This is my path
path = ""

# to store files in a list
list = []

# dirs=directories
for (root, dirs, file) in os.walk(path):
    for f in file:
        print(f)