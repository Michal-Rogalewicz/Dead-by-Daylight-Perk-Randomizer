import random
from colorama import Fore, Style, init
from perks import survivor_perks, exhaustion_perks, healing_perks
init(autoreset=True)

def title():
    print(Fore.CYAN + Style.BRIGHT + "\nDEAD BY DAYLIGHT - PERK RANDOMIZER\n")

def print_build(build):
    print(Fore.WHITE + Style.BRIGHT + "\nYour Perk Build: ")
    for perk in build:
        print(Fore.BLUE + Style.BRIGHT + "- " + perk)

def get_build(perk_pool):
    return random.sample(perk_pool, 4)

def choose_mode():
    print("\n1 - Any\n")
    print("\n2 - Exhaustion\n")
    print("\n3 - Healing\n")

    while True:
        mode = input("Choose your mode: ").strip()

        if mode == "1":
            return survivor_perks
        elif mode == "2":
            return exhaustion_perks
        elif mode == "3":
            return healing_perks
        else:
            print(Fore.WHITE + Style.BRIGHT + "Incorrect Input")

def main():
    title()

    chosen_perks = choose_mode()
    build = get_build(chosen_perks)
    print_build(build)

    while True:
        start = input("[R]reroll, [M]ode [Q]uit: ").lower().strip()

        if start == "r":
            build = get_build(chosen_perks)
            print_build(build)

        elif start == "m":
            chosen_perks = choose_mode()
            build = get_build(chosen_perks)
            print_build(build)

        elif start == "q":
            print("Goodbye")
            break
                
        else:
            print("Try again. \n")

if __name__ == "__main__":
    main()
