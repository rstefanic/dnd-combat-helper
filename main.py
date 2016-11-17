"""
DND COMBAT HELPER

Keep track of players, and create monsters for your DND encounters.
Roll initiatives for monsters in battle, and keep track of who's turn it is.
Mark people as dead, or bleeding out, and tally up the party's EXP.

Robert Stefanic (c) 2016
"""

import sys

from battle import *
from database import *
from colorama import Fore, Back, Style, init

init(autoreset=True)


class Combatant:
    """"Create a monster -or- player object, and set them up to be added to the database"""

    def __init__(self, name, hp, ac, exp=None, init_mod=None, special=False):
        self.name = name
        self.hp = hp
        self.ac = ac
        self.exp = exp
        self.init_mod = init_mod
        self.special = special

    def __str__(self):
        return "{}\t[HP: {}, AC: {}]".format(self.name, self.hp, self.ac)

    def add_monster_to_db(self):
        """Function to add current monster to monster database."""
        Monsters.create(monster_name=self.name, hp=self.hp, ac=self.ac, exp=self.exp,
                        init_mod=self.init_mod, special=self.special)


class Player(Combatant):
    """Create Player Object"""
    def add_fighter_to_db(self):
        """Function to add current object to Players database."""
        Players.create(player_name=self.name, hp=self.hp, ac=self.ac)


def main_loop():
    """Main program loop."""
    while True:
        main_menu()
        user_input = input(">> ").lower().strip()
        if user_input == 'a':
            add_to_db()
        elif user_input == 'i':
            initialize_battle()
        elif user_input == 'q':
            clear()
            print("Good bye!")
            sys.exit()


def main_menu():
    """Display the Main Menu"""
    clear()
    print(Fore.GREEN + "*" * 80)
    print("\t\t\t    " + Style.BRIGHT + "MAIN MENU")
    print(Fore.GREEN + "*" * 80)
    print("\t\tEnter " + Back.WHITE + Fore.BLACK + "'a'" + Back.RESET + Fore.RESET + " to add Fighters to the Database,")
    print("\t\tEnter " + Back.WHITE + Fore.BLACK + "'i'" + Back.RESET + Fore.RESET + " to initialize or start a battle.")
    print("\t\tEnter " + Back.WHITE + Fore.BLACK + "'q'" + Back.RESET + Fore.RESET + " to quit.")


def clear():
    """Clear the screen."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def add_to_db():
    """Add another fighter to the battle."""

    # Set the invalid flag to false
    invalid = False

    while True:
        clear()

        # Print menu
        print(Fore.GREEN + "*" * 80)
        if invalid:
            print("\t\t\t  " + Style.BRIGHT + "ADD FIGHTER\t" + Back.RED + "** INVALID INPUT **")
        else:
            print("\t\t\t  " + Style.BRIGHT + "ADD FIGHTER")
        print(Fore.GREEN + "*" * 80)
        print("\t\tEnter " + Back.WHITE + Fore.BLACK + "'p'" + Back.RESET + Fore.RESET + " to add players to database,")
        print("\t\tEnter " + Back.WHITE + Fore.BLACK + "'m'" + Back.RESET + Fore.RESET + " to add monsters to database,")
        print("\t\tEnter " + Back.WHITE + Fore.BLACK + "'q'" + Back.RESET + Fore.RESET + " to return to main menu.")

        # Ask user for action, do that action
        user_input = input(">> ")
        if user_input == 'p':
            invalid = False
            add_player()
        elif user_input == 'm':
            invalid = False
            add_monster()
        elif user_input == 'q':
            break
        else:
            invalid = True


def add_monster():
    """Add a new monster to the monsters database"""

    def print_monsters_database():
        """Print the Monsters database so the user knows what monsters or characters have been added"""
        monsters = Monsters.select()
        clear()
        print(Fore.GREEN + "*" * 80)
        print("\t\t\t" + Style.BRIGHT + "Monsters Database")
        print("\t\t  " + Style.DIM + "(Monsters in red are special)")
        print(Fore.GREEN + "_" * 80 + "\n")
        for monster in monsters:
            if monster.special:
                print("\t\t\t" + Fore.RED + monster.monster_name)
            else:
                print("\t\t\t" + monster.monster_name)
        print(Fore.GREEN + "_" * 80)
        print(Fore.GREEN + "*" * 80)

    while True:
        # Print all the monsters in the database
        print_monsters_database()

        # Display options, ask for input
        print(Back.WHITE + Fore.BLACK + "[A]" + Back.RESET + Fore.RESET + 'dd a new monster, or ' +
              Back.WHITE + Fore.BLACK + "[Q]" + Back.RESET + Fore.RESET + "uit to go back to the previous menu.")
        user_input = input(">> ").lower()

        # Gather necessary data to add a monster to the database
        if user_input == 'a':
            name = input("Monster Type/Name?\n>> ")
            hp = input("Monster HP?\n>> ")
            ac = input("Monster AC?\n>> ")
            exp = input("Monster EXP?\n>> ")
            init_mod = input("Monster Initiative?\n>> ")
            special = input("Is this monster special? [y/N]\n>> ")
            try:
                Combatant(name, hp, ac, exp, init_mod, special).add_monster_to_db()
            except ValueError:
                input(Fore.RED + "** ERROR: Invalid entries for monster ")

        # Go back a page
        elif user_input == 'q':
            break


def add_player():
    """Add a player to the player database"""

    def print_players_database():
        """Print the Player Database so the user knows everyone who's already been added"""
        players = Players.select()
        clear()
        print(Fore.GREEN + "*" * 80)
        print("\t\t\t  " + Style.BRIGHT + "Players Database")
        print(Fore.GREEN + "_" * 80 + "\n")
        for player in players:
            print("\t\t\t" + player.player_name)
        print(Fore.GREEN + "_" * 80)
        print(Fore.GREEN + "*" * 80)

    while True:
        # Print all the players in the player database
        print_players_database()
        print(Back.WHITE + Fore.BLACK + "[A]" + Back.RESET + Fore.RESET + 'dd new player, or ' +
              Back.WHITE + Fore.BLACK + "[Q]" + Back.RESET + Fore.RESET + "uit to go back to the previous menu.")
        user_input = input(">> ").lower()

        # Gather the necessary information to add a player to the player database
        if user_input == 'a':
            name = input("Player name?\n>> ")
            ac = input("Player AC?\n>> ")
            hp = input("Player HP?\n>> ")
            try:
                Player(name, hp, ac).add_fighter_to_db()
            except ValueError:
                input(Fore.RED + "** ERROR: Invalid entries for player ")

        # Go back a screen
        elif user_input == 'q':
            break


if __name__ == "__main__":
    # Define the terminal dimensions, initialize the database, and start the program
    os.environ['LINES'] = "25"
    os.environ['COLUMNS'] = "80"
    initialize_db()
    main_loop()
