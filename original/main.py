# main.py — original course solution for Day 14: Higher or Lower.
# Everything lives in one file: data, helper functions, and the game loop.
# This is the procedural style taught in the course — no classes, no modules
# beyond the two imports below.

import art      # art.py in this same folder — holds the logo and VS separator
import random   # standard library — used to pick random accounts from the list

# The full dataset of Instagram accounts.
# Each entry is a dict with name, follower_count (in millions), description, and country.
data = [
    {'name': 'Instagram', 'follower_count': 346, 'description': 'Social media platform', 'country': 'United States'},
    {'name': 'Cristiano Ronaldo', 'follower_count': 215, 'description': 'Footballer', 'country': 'Portugal'},
    {'name': 'Ariana Grande', 'follower_count': 183, 'description': 'Musician and actress', 'country': 'United States'},
    {'name': 'Dwayne Johnson', 'follower_count': 181, 'description': 'Actor and professional wrestler', 'country': 'United States'},
    {'name': 'Selena Gomez', 'follower_count': 174, 'description': 'Musician and actress', 'country': 'United States'},
    {'name': 'Kylie Jenner', 'follower_count': 172, 'description': 'Reality TV personality and businesswoman', 'country': 'United States'},
    {'name': 'Kim Kardashian', 'follower_count': 167, 'description': 'Reality TV personality and businesswoman', 'country': 'United States'},
    {'name': 'Lionel Messi', 'follower_count': 149, 'description': 'Footballer', 'country': 'Argentina'},
    {'name': 'Beyoncé', 'follower_count': 145, 'description': 'Musician', 'country': 'United States'},
    {'name': 'Neymar', 'follower_count': 138, 'description': 'Footballer', 'country': 'Brasil'},
    {'name': 'National Geographic', 'follower_count': 135, 'description': 'Magazine', 'country': 'United States'},
    {'name': 'Justin Bieber', 'follower_count': 133, 'description': 'Musician', 'country': 'Canada'},
    {'name': 'Taylor Swift', 'follower_count': 131, 'description': 'Musician', 'country': 'United States'},
    {'name': 'Kendall Jenner', 'follower_count': 127, 'description': 'Reality TV personality and Model', 'country': 'United States'},
    {'name': 'Jennifer Lopez', 'follower_count': 119, 'description': 'Musician and actress', 'country': 'United States'},
    {'name': 'Nicki Minaj', 'follower_count': 113, 'description': 'Musician', 'country': 'Trinidad and Tobago'},
    {'name': 'Nike', 'follower_count': 109, 'description': 'Sportswear multinational', 'country': 'United States'},
    {'name': 'Khloé Kardashian', 'follower_count': 108, 'description': 'Reality TV personality and businesswoman', 'country': 'United States'},
    {'name': 'Miley Cyrus', 'follower_count': 107, 'description': 'Musician and actress', 'country': 'United States'},
    {'name': 'Katy Perry', 'follower_count': 94, 'description': 'Musician', 'country': 'United States'},
    {'name': 'Kourtney Kardashian', 'follower_count': 90, 'description': 'Reality TV personality', 'country': 'United States'},
    {'name': 'Kevin Hart', 'follower_count': 89, 'description': 'Comedian and actor', 'country': 'United States'},
    {'name': 'Ellen DeGeneres', 'follower_count': 87, 'description': 'Comedian', 'country': 'United States'},
    {'name': 'Real Madrid CF', 'follower_count': 86, 'description': 'Football club', 'country': 'Spain'},
    {'name': 'FC Barcelona', 'follower_count': 85, 'description': 'Football club', 'country': 'Spain'},
    {'name': 'David Beckham', 'follower_count': 82, 'description': 'Footballer', 'country': 'United Kingdom'},
    {'name': 'Rihanna', 'follower_count': 81, 'description': 'Musician and businesswoman', 'country': 'Barbados'},
    {'name': 'Demi Lovato', 'follower_count': 80, 'description': 'Musician and actress', 'country': 'United States'},
    {'name': "Victoria's Secret", 'follower_count': 69, 'description': 'Lingerie brand', 'country': 'United States'},
    {'name': 'Zendaya', 'follower_count': 68, 'description': 'Actress and musician', 'country': 'United States'},
    {'name': 'Cardi B', 'follower_count': 67, 'description': 'Musician', 'country': 'United States'},
    {'name': 'Shakira', 'follower_count': 66, 'description': 'Musician', 'country': 'Colombia'},
    {'name': 'Drake', 'follower_count': 65, 'description': 'Musician', 'country': 'Canada'},
    {'name': 'Chris Brown', 'follower_count': 64, 'description': 'Musician', 'country': 'United States'},
    {'name': 'LeBron James', 'follower_count': 63, 'description': 'Basketball player', 'country': 'United States'},
    {'name': 'Vin Diesel', 'follower_count': 62, 'description': 'Actor', 'country': 'United States'},
    {'name': 'Billie Eilish', 'follower_count': 61, 'description': 'Musician', 'country': 'United States'},
    {'name': 'Justin Timberlake', 'follower_count': 59, 'description': 'Musician and actor', 'country': 'United States'},
    {'name': 'UEFA Champions League', 'follower_count': 58, 'description': 'Club football competition', 'country': 'Europe'},
    {'name': 'Shawn Mendes', 'follower_count': 57, 'description': 'Musician', 'country': 'Canada'},
    {'name': 'NASA', 'follower_count': 56, 'description': 'Space agency', 'country': 'United States'},
    {'name': 'Emma Watson', 'follower_count': 56, 'description': 'Actress', 'country': 'United Kingdom'},
    {'name': 'Virat Kohli', 'follower_count': 55, 'description': 'Cricketer', 'country': 'India'},
    {'name': 'Gigi Hadid', 'follower_count': 54, 'description': 'Model', 'country': 'United States'},
    {'name': 'Priyanka Chopra Jonas', 'follower_count': 53, 'description': 'Actress and musician', 'country': 'India'},
    {'name': '9GAG', 'follower_count': 52, 'description': 'Social media platform', 'country': 'China'},
    {'name': 'Ronaldinho', 'follower_count': 51, 'description': 'Footballer', 'country': 'Brasil'},
    {'name': 'Maluma', 'follower_count': 50, 'description': 'Musician', 'country': 'Colombia'},
    {'name': 'Camila Cabello', 'follower_count': 49, 'description': 'Musician', 'country': 'Cuba'},
    {'name': 'NBA', 'follower_count': 47, 'description': 'Club Basketball Competition', 'country': 'United States'},
]


def format_data(account):
    """Takes an account dict and returns a human-readable string for display."""
    account_name = account["name"]
    account_descr = account["description"]
    account_country = account["country"]
    # Example output: "Taylor Swift, a Musician, from United States"
    return f"{account_name}, a {account_descr}, from {account_country}"


def check_answer(u_guess, a_foll, b_foll):
    """Returns True if the player's guess matches which account has more followers.

    Tie rule: if both follower counts are equal, any guess is accepted as correct.
    """
    # Tie: counts match, player gets the point regardless of their guess
    if a_foll == b_foll:
        print("Both accounts have (roughly) the same number of followers. You still get the point ;)")
        return True

    # If A has more followers, the correct guess is "a", and vice versa.
    if a_foll > b_foll:
        return u_guess == "a"
    else:
        return u_guess == "b"


# --- Game setup ---
print(art.logo)   # print the ASCII title art before the game starts

current_score = 0

# Pick two random starting accounts.
# Note: there's no duplicate check here, so A and B could theoretically be the same.
a = random.choice(data)
b = random.choice(data)

game_at_play = True  # flag that controls the main game loop

# --- Main game loop ---
while game_at_play:

    # Show both accounts to the player
    print(format_data(a))
    print(art.vs)   # ASCII "VS" separator
    print(format_data(b))

    # Input validation loop: keep asking until the player types 'a' or 'b'
    user_answered = False
    while not user_answered:
        user_guess = input("Who has more followers? Type 'A' or 'B': ").lower()
        if user_guess == 'a' or user_guess == 'b':
            user_answered = True
        else:
            print("Please enter a valid answer.")

    # Extract follower counts to pass into check_answer
    a_followers = a['follower_count']
    b_followers = b['follower_count']

    is_correct = check_answer(user_guess, a_followers, b_followers)

    if is_correct:
        current_score += 1
        # Clear the screen by printing 25 blank lines before showing the result.
        # (The advanced version uses os.system("clear") for a cleaner approach.)
        print('\n' * 25)
        print(f"You're right! Current score: {current_score}")

        # "B becomes the new A" — this is the key mechanic.
        # The player already knows B's follower count, so it stays on screen
        # as the known quantity while a fresh unknown B is drawn.
        a = b
        b = random.choice(data)
    else:
        print(f"I'm sorry, you guessed incorrectly. Your final score was: {current_score}")
        game_at_play = False  # break out of the while loop
