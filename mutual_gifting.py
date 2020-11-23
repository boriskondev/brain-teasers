import random

names = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

pairs = []

while names:
    gift_from = names[0]
    gift_to = random.choice(names[1:])
    if gift_from != gift_to:
        pair = (gift_from, gift_to)
        pairs.append(pair)
        names = names[1:]
        names.remove(gift_to)

[print(f"{pair[0]} --> {pair[1]}") for pair in pairs]