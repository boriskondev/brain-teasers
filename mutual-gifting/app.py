import csv
import random
from email.message import EmailMessage
import smtplib
import pandas
import docx

contacts = docx.Document("db_test.docx")

names = []
people_to_award = []

fractions = ["влезеш в моите маркови ботуши",
             "яхнеш шейната ми с 10 еленски сили",
             "нахлузиш ръкавиците ми против сняг и студ",
             "ръчкаш Рудолф с остена",
             "се шмугнеш в опушения комин",
             "си лепнеш моята секси бяла брада",
             "получиш моя личен Червен сертификат",
             "ме заместиш, като разказваш мръсни вицове на Снежанка"]

password = input("Email pass: ")
email_sender = "emails.tasting@gmail.com"
email_in_cc = "emails.tasting@gmail.com"

for paragraph in contacts.paragraphs:
    name_and_email = paragraph.text.split(", ")
    names.append(name_and_email)
    people_to_award.append(name_and_email[0])

pairs = []

while names:
    giver = names[0]
    gift_from = giver[0]
    gift_to = random.choice(people_to_award)
    if gift_from != gift_to:
        pair = (giver, gift_to)
        pairs.append(pair)
        people_to_award.remove(gift_to)
        names = names[1:]

report = [f"{pair[0][0]} ({pair[0][1]}) > {pair[1]}" for pair in pairs]

[print(r) for r in report]

for pair in pairs:
    email_receiver_name = pair[0][0]
    email_receiver_contact = pair[0][1]
    gift_receiver_name = pair[1]

    greeting_fraction = random.choice(fractions)

    message = EmailMessage()
    message["Subject"] = f"{email_receiver_name}, открий на кого си ТАЕН ДЯДО КОЛЕДА"
    message["From"] = email_sender
    message["To"] = email_receiver_contact

    message.set_content(f"""\
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            
            <title>Време е за подаръци!</title>
        </head>
        <body style="margin: 0;padding: 0;box-sizing: border-box">
        <section style="margin: 0 15px;">
            <p>Здравей, {email_receiver_name}.</p>
            <p>Тази година ще {greeting_fraction} и ще зарадваш с подарък... <strong>{gift_receiver_name}</strong>!</p>
            <p>Лимитът на подаръка е <strong>30 лева</strong>, а размяната ще се състои на <strong>21 декември</strong> (TBD).</p>
            <p>Хо-хо-хо и весела Коледа от Лапландия, </p>
            <p>Дядо Коледа</p>
        </section>
        </body>
        </html>
    """, subtype="html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_sender, password)
        server.send_message(message)
