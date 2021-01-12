def yes_or_no():
    attempts = 0
    positives = ["yes", "ye", "y"]
    negatives = ["no", "n"]
    while True:
        user_input = input("Yes/No: ").lower()
        if user_input in positives:
            user_input = "yes"
            break
        elif user_input in negatives:
            user_input = "no"
            break
        else:
            attempts += 1
            if attempts != 5:
                print()
                print("Not a valid answer. Try again.", end=" ")
            elif attempts == 5:
                print()
                print(f"You made {attempts} wrong attempts.\n\nDo you want to take a break?", end=" ")
                user_input = input("Yes/No: ").lower()
                if user_input in positives:
                    print("We all have our moments. See you soon.")
                    quit()
                elif user_input in negatives:
                    print()
                    print("Let's try again then.", end=" ")
                    attempts = 0
                    continue
    return user_input
