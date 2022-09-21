# https://www.telecomhall.net/t/sending-email-with-python/14314

import win32com.client as win32

# Construct Outlook application instance
olApp = win32.Dispatch("Outlook.Application")
olNS = olApp.GetNameSpace("MAPI")

# File name removed for safe reasons
pairs_file = ""
pairs = []

i = 1

with open(pairs_file) as f:
    [pairs.append(line.strip()) for line in f.readlines()]

for pair in pairs:

    redundant_string, emails = pair.split(": ")
    emails = emails.split(" + ")

    # Construct the email item object
    mailItem = olApp.CreateItem(0)
    mailItem.Subject = f"Mystery Coffee pair {i}"
    mailItem.BodyFormat = 1
    mailItem.Body = f"Hello from the other side {i}"
    mailItem.To = ";".join(emails)
    mailItem.Display()

    mailItem.Save()
    mailItem.Send()

    i += 1
