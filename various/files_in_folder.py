# import OS module
import os

# This is my path
path = "C://Users//boris.kondev//OneDrive - Do IT Wise Bulgaria//Desktop//Docs//Misc//_TBD//Навсякъде, където те няма"

# to store files in a list
list = []

# dirs=directories
for (root, dirs, file) in os.walk(path):
    for f in file:
        print(f)