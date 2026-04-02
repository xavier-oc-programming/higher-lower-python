import art
import random
import game_data


def format_data(account):
    """Takes the account data and returns the printable format."""
    account_name = account["name"]
    account_descr = account["description"]
    account_country = account["country"]
    return f"{account_name}, a {account_descr}, from {account_country}"


def check_answer(u_guess, a_foll, b_foll):
    """Takes the account data and returns it in a printable format."""
    if a_foll == b_foll:
        print("Both accounts have (roughly) the same number of followers. You still get the point ;) ")
        return True
    if a_foll > b_foll:
        return u_guess == "a"
    else:
        return u_guess == "b"


def first_a_and_b():
    first_a = random.choice(game_data.data)

    first_b = random.choice(game_data.data)
    return first_a, first_b


print(art.logo)

current_score = 0
a, b = first_a_and_b()

game_at_play = True

while game_at_play:

    print(format_data(a))
    print(art.vs)
    print(format_data(b))
    # print(f'\nA\'s follower count: {a["follower_count"]}')
    # print(f'B\'s follower count: {b["follower_count"]}\n')

    user_answered = False
    while not user_answered:
        user_guess = input("Who has more followers? Type 'A' or 'B': ").lower()
        if user_guess == 'a' or user_guess == 'b':
            user_answered = True
        else:
            print("Please enter a valid answer.")

    # checking answer
    # extract follower amounts
    a_followers = a['follower_count']
    b_followers = b['follower_count']

    # print(f'A\'s follower count: {a_followers}')
    # print(f'B\'s follower count: {b_followers}')

    is_correct = check_answer(user_guess, a_followers, b_followers)
    if is_correct:
        current_score += 1
        print('\n'*25)
        print(f"You're right! Current score: {current_score}")
        a = b
        b = random.choice(game_data.data)
    else:
        print(f"I\'m sorry, you guessed incorrectly. Your final score was: {current_score} ")
        game_at_play = False





