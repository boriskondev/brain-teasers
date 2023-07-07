import pandas as pd
import win32com.client as win32

# How to send PLAIN TEXT EMAIL from Outlook using Python - https://youtu.be/OPiBtQxELSU

# Read CSV file into a pandas DataFrame
df = pd.read_csv('emails.csv')

# Connect to Outlook and create a mail item
outlook = win32.Dispatch('Outlook.Application')
mail = outlook.CreateItem(0)
# mail.Display()

# Retrieve the list of accounts available in Outlook
accounts = outlook.Session.Accounts

# Loop through the accounts and find the one we want to use
for account in accounts:
    if account.SmtpAddress == 'info@company.com':
        # If we find the desired account, set it as the sending account for the mail item
        mail._oleobj_.Invoke(*(64209, 0, 8, 0, account))
        break

# Loop through email pairs in the DataFrame
for index, row in df.iterrows():
    # Extract email addresses from the current row
    to_emails = row[0].split(' + ')

    # Set the email properties
    mail.To = to_emails[0] + ';' + to_emails[1]  # Set the recipients
    mail.Subject = 'Subject'  # Set the subject
    mail.Body = 'Body'  # Set the body of the email
    mail.Attachments.Add('attachment.pdf')  # Add an attachment (if desired)

    # Send the email
    mail.Send()

# Close the Outlook application
outlook.Quit()

