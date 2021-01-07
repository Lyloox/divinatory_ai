from divinatory_ai.spreads import get_spreads_dict
from divinatory_ai import utils


def guide():
    while True:
        spreads = get_spreads_dict()
        print(utils.ascii_cat_welcome())
        print("What do you want to know?")
        for i, question in enumerate(spreads.keys()):
            print(f"{i}: {question}")
        user_spread = input()
        try:
            user_spread = int(user_spread)
            user_spread = list(spreads.keys())[user_spread]
        except (ValueError, KeyError):
            print("You wanna stop? Ok, see you later :)")
            break
        print(f"Okay, I got you want a {user_spread} spread. "
              f"Can you write a specific question? ")
        user_question = input()
        function, args = spreads[user_spread]
        function(*args)


if __name__ == '__main__':
    guide()
