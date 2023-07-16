import random

def pick_one(texts):
    return random.choice(texts)

def pick_one_by_prompt(texts):
    valid_selection = None
    while (not valid_selection):
        print(texts)
        selected = input("Please pick one >>")
        if (selected in texts):
            valid_selection = selected
    return valid_selection
