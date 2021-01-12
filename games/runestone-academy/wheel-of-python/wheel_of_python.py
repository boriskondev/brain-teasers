import json
import random
import time


class WOFPlayer:
    def __init__(self, name, prize_money=0, prizes=[]):
        self.name = name
        self.prize_money = prize_money
        self.prizes = prizes

    def add_money(self, amt):
        self.prize_money = self.prize_money + amt

    def go_bankrupt(self):
        self.prize_money = 0

    def add_prize(self, prize):
        self.prizes.append(prize)

    def __str__(self):
        return f"{self.name} (&{self.prize_money})"


class WOFHumanPlayer(WOFPlayer):
    def __init__(self, name, prize_money=0, prizes=[]):
        WOFPlayer.__init__(self, name, prize_money, prizes)

    def get_move(self, category, obscured_phrase, guessed):
        WOFPlayer.__str__(self)
        prompt = input(f"{self.name} has &{self.prize_money}"
                       f"\nCategory: {category}"
                       f"\nPhrase:  {obscured_phrase}"
                       f"\nGuessed: {guessed}"
                       f"\nGuess a letter, phrase, or type 'exit' or 'pass': ")
        return prompt


class WOFComputerPlayer(WOFPlayer):

    SORTED_FREQUENCIES = "ZQXJKVBPYGFWMUCLDRHSNIOATE"

    def __init__(self, name, difficulty, prize_money=0, prizes=[]):
        WOFPlayer.__init__(self, name, prize_money, prizes)
        self.difficulty = difficulty

    def smart_coin_flip(self):
        rand_num = random.randint(1, 10)
        if rand_num > self.difficulty:
            return True
        else:
            return False

    def get_possible_letters(self, guessed):
        if self.prize_money < VOWEL_COST:
            letters_to_guess = [letter for letter in LETTERS if letter not in VOWELS and letter not in guessed]
        else:
            letters_to_guess = [letter for letter in LETTERS if letter not in guessed]
        return letters_to_guess

    def get_move(self, category, obscured_phrase, guessed):
        computer_move = ""
        print(f"{self.name} has &{self.prize_money}"
                       f"\nCategory: {category}"
                       f"\nPhrase:  {obscured_phrase}"
                       f"\nGuessed: {guessed}"
                       f"\nThe computer is taking a move.")
        what_to_guess = self.get_possible_letters(guessed)
        if len(what_to_guess) == 0:
            computer_move = "pass"
        coin_flip = self.smart_coin_flip()
        if coin_flip:
            computer_move = self.SORTED_FREQUENCIES[-1]
            self.SORTED_FREQUENCIES = self.SORTED_FREQUENCIES[:-1]
        else:
            computer_move = random.choice(what_to_guess)
        return computer_move


LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
VOWELS = "AEIOU"
VOWEL_COST = 250


def get_number_between(prompt, min_num, max_num):
    user_input = input(prompt)

    while True:
        try:
            n = int(user_input)
            if n < min_num:
                error_message = f"Must be at least {min_num}"
            elif n > max_num:
                error_message = f"Must be at most {max_num}"
            else:
                return n
        except ValueError:
            error_message = f"{user_input} is not a number."

        user_input = input(f"{error_message}\n{prompt}")


def spin_wheel():  # Spins the wheel of fortune wheel to give a random prize
    with open("wheel.json", 'r') as f:
        wheel = json.loads(f.read())
        return random.choice(wheel)


def get_random_category_and_phrase():  # Returns a category & phrase (as a tuple) to guess
    with open("phrases.json", 'r') as f:
        phrases = json.loads(f.read())
        category = random.choice(list(phrases.keys()))
        phrase = random.choice(phrases[category])
        return category, phrase.upper()


def obscure_phrase(phrase, guessed):  # Given a phrase and a list of guessed letters, returns an obscured version
    rv = ''
    for s in phrase:
        if (s in LETTERS) and (s not in guessed):
            rv = rv+'_'
        else:
            rv = rv+s
    return rv


def show_board(category, obscured_phrase, guessed):  # Returns a string representing the current state of the game
    return f"""
Category: {category}
Phrase:   {obscured_phrase}
Guessed:  {', '.join(sorted(guessed))}"""


# GAME LOGIC CODE
print("=" * 15)
print("WHEEL OF PYTHON")
print("="*15)
print()

num_human = get_number_between("How many human players? ", 0, 10)
num_computer = get_number_between("How many computer players? ", 0, 10)

if num_computer >= 1:
    difficulty = get_number_between("What difficulty for the computers? (1-10) ", 1, 10)

human_players = [WOFHumanPlayer(input(f"Enter the name for player #{i + 1}: ")) for i in range(num_human)]
computer_players = [WOFComputerPlayer(f"Computer {i + 1}", difficulty) for i in range(num_computer)]
players = human_players + computer_players

if len(players) == 0:
    print("We need players to play!")
    raise Exception

category, phrase = get_random_category_and_phrase()

guessed = []

player_index = 0

winner = False

while True:
    player = players[player_index]
    wheel_prize = spin_wheel()

    print("-" * 15)
    print(show_board(category, obscure_phrase(phrase, guessed), guessed))
    print()
    print(f"{player.name} spins...")
    time.sleep(2)
    print(f"{wheel_prize['text']}")

    if wheel_prize["type"] == "bankrupt":
        player.go_bankrupt()
    elif wheel_prize["type"] == "cash":
        move = player.get_move(category, obscure_phrase(phrase, guessed), guessed)
        move = move.upper()
        if move == "EXIT":
            break
        elif move != "PASS":
            if len(move) == 1:
                if move not in LETTERS:
                    print("Guesses should be alphanumeric. Try again.")
                    continue
                if move in guessed:
                    print(f"{move} has already been guessed. Try again.")
                    continue

                if move in VOWELS:
                    if player.prize_money < VOWEL_COST:
                        print(f"Need {VOWEL_COST} to guess a vowel. Try again.")
                        continue
                    else:
                        player.prize_money -= VOWEL_COST

                guessed.append(move)

                print(f"{player.name} says '{move}'")

                count = phrase.count(move)
                if count > 0:
                    if count == 1:
                        print(f"There is one {move}")
                    else:
                        print(f"There are {count} {move}'s")

                    player.add_money(count * wheel_prize["value"])

                    if wheel_prize["prize"]:
                        player.add_prize(wheel_prize["prize"])

                    if obscure_phrase(phrase, guessed) == phrase:
                        winner = player
                        break

                    continue

                elif count == 0:
                    print(f"There is no {move}")
            else:
                if move == phrase:
                    player.add_money(wheel_prize["value"])
                    if wheel_prize["prize"]:
                        player.add_prize(wheel_prize["prize"])
                    winner = player
                    break
                else:
                    print(f"{move} was not the phrase")

    # Move on to the next player (or go back to player[0] if we reached the end)
    player_index = (player_index + 1) % len(players)

if winner:
    print(f"{winner.name} wins! The phrase was {phrase}")
    print(f"{winner.name} won ${winner.prize_money}")
    if len(winner.prizes) > 0:
        print(f"{winner.name} also won:")
        for prize in winner.prizes:
            print(f"    - {prize}")
else:
    print("Nobody won.")
