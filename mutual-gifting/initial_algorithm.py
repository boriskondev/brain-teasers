import random

names = ["Dancho", "Boris", "Ilona", "Katerina", "Kristiyan", "Stefka",
         "Vesko", "Hilda", "Milena", "Martin", "Martina", "Sonya"]

people_to_award = names[:]

pairs = []

while names:
    gift_from = names[0]
    gift_to = random.choice(people_to_award)
    if gift_from != gift_to:
        pair = (gift_from, gift_to)
        pairs.append(pair)
        people_to_award.remove(gift_to)
        names = names[1:]

[print(f"{pair[0]} buys gift to {pair[1]}!") for pair in pairs]
