import random
import functions
import categories
import gallows
from datetime import datetime
import pandas as pd
import os

games_played = 0
hint_counter = 0
words_to_import = ""

while True:
    lives = 6

    # Starting the game
    if games_played > 0:
        print()
        print("Welcome back again.")
        print()
    else:
        print()
        print("--- Welcome to Boris Kondev's interpretation of Hangman, inspired by Finxter.com! ---")
        print()
        print("Before you begin please read the following instructions:")
        print(
            f"- You have {lives} lives to go."
            f"\n- Use lowercase English letters only."
            f"\n- Some guesses consist of more than one word."
            "\n- Some words have one or more special characters in them.")
        print()

    # Category selection
    print("Which category would you like to be challenged with?")
    [print(f"{n}. {c}") for (n, c) in enumerate(categories.categories.keys(), 1)]
    categories_list = [k for k, v in categories.categories.items()]
    while True:
        category_choice = int(input("Choose the number of the category: "))
        print()
        if category_choice < 1 or category_choice > len(categories_list):
            print("Not a valid choice. Please try again.")
            continue
        else:
            if category_choice == len(categories_list):
                words_to_import = [value for values in categories.categories.values() for value in values]
            else:
                words_to_import = categories.categories[categories_list[category_choice - 1]]
            break

    # Difficulty selection by user
    difficulties = ["Easy", "Medium", "Hard"]
    print("Which difficulty do you prefer to play?")
    [print(f"{n}. {c}") for (n, c) in enumerate(difficulties, 1)]
    while True:
        difficulty_choice = int(input("Choose the number of the difficulty: "))
        print()
        if difficulty_choice < 1 or difficulty_choice > len(difficulties):
            print("Not a valid choice. Please try again.")
            continue
        else:
            break

    # Difficulty step calculation
    min_length = min([len(x) for x in words_to_import])
    max_length = max([len(x) for x in words_to_import])
    difficulty_step = (max_length - min_length) // 3

    # Word to play selection based on the selected difficulty
    if difficulty_choice == 1:
        words_to_import = list(filter(lambda x: len(x) <= difficulty_step, words_to_import))
    elif difficulty_choice == 2:
        words_to_import = list(filter(lambda x: difficulty_step < len(x) <= difficulty_step * 2, words_to_import))
    elif difficulty_choice == 3:
        words_to_import = list(filter(lambda x: difficulty_step * 2 < len(x), words_to_import))

    string_to_guess = random.choice(words_to_import)
    successful_guess = string_to_guess
    string_to_guess = string_to_guess.lower()

    #print("---")
    #print(string_to_guess)
    #print("---")

    guessed_so_far = "_" * len(string_to_guess)

    for index in range(len(string_to_guess)):
        if string_to_guess[index] == " ":
            guessed_so_far = guessed_so_far[:index] + " " + guessed_so_far[index + 1:]

    if len(guessed_so_far.split()) == 1:
        word = "word"
    else:
        word = "phrase"

    print(f"Your {word} to guess is: \"{guessed_so_far}\".")
    print()
    print("Ready to play?", end=" ")
    ready_prompt = functions.yes_or_no()
    print()
    if ready_prompt == "yes":
        print("Good luck! The clock starts ticking.")
        time_start = datetime.now()
    else:
        print("We all have our moments. See you soon.")
        quit()

    already_played_list = []

    game_start = True

    # Main game loop
    while True:
        if game_start:
            print(gallows.graphic[lives])

        game_start = False
        right_guess = False

        users_guess = input("Guess a letter: ").lower()

        if users_guess == " ":
            print(f"If any, the spaces are already included in the {word}.")
            print()
            continue

        if users_guess in already_played_list:
            print("You already played this", end=" ")
            if users_guess in guessed_so_far:
                print("and it was correct.")
                print()
            else:
                print("and it was wrong.")
                print()
            continue
        else:
            already_played_list.append(users_guess)

        for index in range(len(string_to_guess)):
            if string_to_guess[index] == users_guess:
                guessed_so_far = guessed_so_far[:index] + users_guess + guessed_so_far[index + 1:]
                right_guess = True

        if right_guess:
            print("That's correct!")
            print()
        else:
            lives -= 1
            print("No such letter. You lost one life.")
            print(gallows.graphic[lives])

            if lives == 0:
                break

            if lives == 3 or lives == 1:
                if lives == 3:
                    print(f"You have {lives} lives left.", end=" ")
                elif lives == 1:
                    print(f"You have {lives} life left.", end=" ")
                print("Would you like to take a hint?\n"
                      "It will add 30 seconds to your total time if you beat the game.")
                hint_prompt = functions.yes_or_no()
                if hint_prompt == "yes":
                    hint_indices = []
                    hint_counter += 1
                    [hint_indices.append(i) for i in range(len(guessed_so_far)) if guessed_so_far[i] == "_"]
                    hint_index = random.choice(hint_indices)
                    hint = ""
                    for i in range(len(string_to_guess)):
                        if hint_index == i:
                            hint = string_to_guess[i]
                            break
                    print()
                    print(f"Your hint is \"{hint}\". Use it wisely!")
                    print()
                    continue
                else:
                    print()
                    print("That is very brave of you! I wish you luck.")
                    print()
                    continue

        if "_" not in guessed_so_far:
            break

        if len(set(guessed_so_far)) == 1:
            continue

        output = ""
        for char in guessed_so_far:
            output = output + char + " "

        print(output)
        print()

    time_end = datetime.now()

    # Endgame message after exiting the main game loop
    if lives > 0:
        print(f"Congratulations. You guessed \"{successful_guess}\" and won!")
        print()
        print("Do you want to be inducted in the Hangman Hall of Fame?", end=" ")
        leaderboard_prompt = functions.yes_or_no()
        if leaderboard_prompt == "yes":
            print()
            print("That's great! Please enter your data.")
            first_name = input("First name: ")
            last_name = input("Last name: ")
            if difficulty_choice == 1:
                difficulty = "Easy"
            elif difficulty_choice == 2:
                difficulty = "Medium"
            elif difficulty_choice == 3:
                difficulty = "Hard"
            score = (time_end - time_start).seconds + hint_counter * 30
            date = datetime.now().date().strftime("%d %B %Y")
            time = time_end.strftime("%H:%M:%S")

            if not os.path.isfile("leaderboard.xlsx"):
                name = [[first_name, last_name, difficulty, score, date, time]]
                leaderboard_df = pd.DataFrame(name, columns=["First name", "Last name", "Difficulty", "Score", "Date", "Time"])
                leaderboard_df.insert(0, "Rank", "1")
                leaderboard_df.to_excel("leaderboard.xlsx", index=False)
                print("Done!", end="")
            else:
                leaderboard_df = pd.read_excel("leaderboard.xlsx", sheet_name=0, skiprows=None)
                leaderboard_df.pop("Rank")
                leaderboard_df = leaderboard_df.append({
                    "First name": first_name,
                    "Last name": last_name,
                    "Difficulty": difficulty,
                    "Score": score,
                    "Date": date,
                    "Time": time}, ignore_index=True, )
                leaderboard_df = leaderboard_df.replace({'Difficulty': {"Hard": 1, "Medium": 2, "Easy": 3}})
                leaderboard_df.sort_values(by=["Difficulty", "Score"], ascending=[True, True], inplace=True)
                leaderboard_df = leaderboard_df.replace({'Difficulty': {1: "Hard", 2: "Medium", 3: "Easy"}})
                leaderboard_df = leaderboard_df.reset_index(drop=True)
                rows = (leaderboard_df.shape[0])
                ranks = []
                [(ranks.append(i + 1)) for i in range(rows)]
                leaderboard_df.insert(0, "Rank", ranks)
                leaderboard_df.to_excel("leaderboard.xlsx", index=False)
                print()
                print("Done!")
    else:
        print("You lost. Train harder to beat the game next time!")

    # Play again prompt
    print()
    print("Let's play another game?", end=" ")
    play_again_prompt = functions.yes_or_no()
    if play_again_prompt == "yes":
        games_played += 1
        hint_counter = 0
        continue
    else:
        print()
        print("Thank you for playing. See you again soon.")
        quit()