# https://www.telecomhall.net/t/sending-email-with-python/14314

import win32com.client as win32

# Construct Outlook application instance
olApp = win32.Dispatch("Outlook.Application")
olNS = olApp.GetNameSpace("MAPI")

# File name removed for safe reasons
pairs_file = "test.txt"
pairs = []

# i = 1

with open(pairs_file) as f:
    [pairs.append(line.strip()) for line in f.readlines()]

for pair in pairs:

    redundant_string, emails = pair.split(": ")
    emails = emails.split(" + ")

    # Construct the email item object
    email = olApp.CreateItem(0)
    email.Subject = f"Congrats_Mystery Coffee Buddy"
    # email.Subject = f"Mystery Coffee pair {i}"
    email.BodyFormat = 1
    # email.Body = f"Hello from the other side {i}"
    email.HTMLBody = """
    <p>Good day to both of you 🌞</p>
    <p>Thank you for taking part in our Mystery Coffee.</p>
    <p>I am so excited to let you know that you two were randomly selected to have a “Coffee meeting” 🥐☕/🍟🍻.</p>
    <p>You could meet whenever you’d like during this month and talk about whatever you want to. </p>
    <p>Enjoy, have fun and taka a picture 😝</p>
    <p>If you need anything, we are here for you!  </p>
    """
    email.To = ";".join(emails)
    email.Display()

    email.Save()
    email.Send()

    # i += 1
