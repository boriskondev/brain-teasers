import csv
import random
from email.message import EmailMessage
import smtplib
import pandas
import docx

password = input("Email password: ")
email_sender = "emails.tasting@gmail.com"
email_in_cc = "emails.tasting@gmail.com"

contacts = docx.Document("db.docx")

names = []
people_to_award = []

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

report = [f"{pair[0][0]} with email {pair[0][1]} to {pair[1]}." for pair in pairs]

[print(r) for r in report]

for pair in pairs:
    email_receiver_name = pair[0][0]
    email_receiver_contact = pair[0][1]
    gift_receiver_name = pair[1]

    message = EmailMessage()
    message["Subject"] = f"Подаръци ще има за всички от сърце!"
    message["From"] = email_sender
    message["To"] = email_receiver_contact

    message_content = f"Здравей, {email_receiver_name}," \
                      f"\nТази година ще зарадваш с подарък {gift_receiver_name}!" \
                      f"\nПоздрави,\nДядо Коледа" \
                      f"\n*Лимит на подаръците: 25 лв. Дядо Коледа©; е запазена марка на The Coca-Cola Company. Всички останали марки са собственост на съответните им притежатели. Период на промоцията: до 10 декември 2020 г."

    message.set_content(message_content)

    message.add_alternative(f"""\
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Title</title>
        </head>
        <body>
            <p>Здравей, {email_receiver_name},</p>
            <p>Тази година ще зарадваш с подарък {gift_receiver_name}!</p>
            <p>Поздрави,</p>
            <p>Дядо Коледа</p>
            <p style="font-size: 10px; ">*Лимит на подаръците: 25 лв. Дядо Коледа&#169; е запазена марка на The Coca-Cola Company. Всички останали марки са собственост на съответните им притежатели. Период на промоцията: до 10 декември 2020 г.</p>
        </body>
        </html>
    """, subtype="html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_sender, password)
        server.send_message(message)

# Хилда Сл, h.baramova@publicis-dialog.bg
# Хилда Л, hildabaramova@gmail.com
# Марто Сл, m.tonev@publicis-dialog.bg
# Марто Л, martotonev@gmail.com
