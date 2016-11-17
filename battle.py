"""
The Battle Screen

The battle screen is where players are added to combat,
initiatives are rolled, players are ordered in their based
on their initiative rolls, and the combat order is executed.


Note: The screen is an object that constantly modifies itself.
"""

import random
import os

from database import *
from colorama import Fore, Style, init

init(autoreset=True)

# List that holds all of the current fighters
battle_list = []


class Screen:
    """The object to set up the screen, and change the screen"""

    """ There are twenty lines between the header and the footer,
        so to keep it consistent, this value tracks the number of lines"""
    lines = 20
    show_numbers = False

    def print_screen(self, lines, options="[A]dd, [I]nitialize Battle, [Q]uit.\n>> ", show_numbers=False):
        """This method prints the screen. The screen clears itself every time, prints all of the current
        fighters, and the displays the options at the bottom followed by a prompt that will
        always return. The default options are set here in the arguments, but it changes
        depending on where the method is called."""

        self.clear()
        print(Fore.GREEN + "*" * 80)
        print("\t\t\t\t    " + Style.BRIGHT + "BATTLE")
        print(Fore.GREEN + "*" * 80)
        print("*")

        for fighter in battle_list:

            # Check to see if the numbers next to their names should be shown
            if not show_numbers:
                print("*\t\t", end='')
            else:
                print("*\t{}\t".format(battle_list.index(fighter) + 1), end='')

            # Players are green, NPCs are white
            if fighter['player'] and fighter['turn']:
                print(">>\t" + Fore.GREEN + fighter['name'])
            elif fighter['player']:
                print("\t" + Fore.GREEN + fighter['name'])
            elif fighter['turn']:
                print(">>\t" + fighter['name'])
            else:
                print("\t" + fighter['name'])

        for i in range(1, lines):
            print("*")

        print(Fore.GREEN + "*" * 80)

        """Prompt user for input, and return that input in lowercase"""
        return input(options).lower()

    @staticmethod
    def clear():
        """Clear the screen"""
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    @staticmethod
    def roll_init():
        """Roll the initiative, then sort the fighters into the correct order"""
        for fighter in battle_list:
            if not fighter['player']:
                fighter['init'] += random.randrange(1, 20)

        for fighter in battle_list:
            if fighter['player']:
                print("What is {}'s initiative?".format(fighter['name']))
                fighter['init'] = input("\n>> ")

    def reverse_bubble_sort_list(self):
        """This bubble sort sorts the list backwards -- The highest number comes first.
        This is because we want the player with the highest initiative to come first in
        the list, while those with a lower initiative score are at the bottom of the list"""

        """Set the variables for the bubble sort:
        successful - Check and see if the sort is finished
        length - length of the entire list (minus 1 to compensate for 0 index start
        i - to iterate through the list"""
        successful = True
        length = len(battle_list) - 1
        i = 0

        while i < length:
            fighter1 = battle_list[i]
            fighter2 = battle_list[i + 1]
            if int(fighter1['init']) < int(fighter2['init']):  # Compare two values
                swap = fighter1                                # If the left value is smaller, swap the two values
                battle_list[i] = fighter2
                battle_list[i + 1] = swap
                successful = False                             # Set successful to false because a swap occurred
            i += 1

        if not successful:
            self.reverse_bubble_sort_list()

    def add_fighters_to_battle_list(self):
        """Add monsters and players to the battle list"""

        print("Add [P]layer or [M]onster to current fight? [q] to back.")
        while True:
            user_input = input(">> ").lower()

            if user_input == 'p':

                # Print all of the players for selection from the players database
                print("\n")
                for player in Players:
                    print("{}: {}".format(player.id, player.player_name))

                user_input = input("\nType the number of the fighter you would like to add or [q] to back."
                                   "\n>> ").lower()

                if user_input == 'q':
                    break
                else:
                    try:
                        """Try and retrieve the player's information based on the player's id.
                        If it doesn't exist, then complain to the user. If it does exist, then add
                        that player, and subtract a line from the screen"""

                        player = Players.get(Players.id == user_input)
                        print(player.player_name + "\n\n\n")
                        battle_list.append({"name": player.player_name, "player": True,
                                            "init": None, "turn": False})

                    except Players.PlayersDoesNotExist:
                        print(Fore.RED + "** Invalid entry. That player does not exist")

                    else:
                        self.lines -= 1
                        break

            elif user_input == 'm':

                # Print all of the monsters for selection from the monster database
                print("\n")
                for monster in Monsters:
                    if monster.special:
                        print("{}: ".format(monster.id) + Fore.RED + "{}".format(monster.monster_name))

                    else:
                        print("{}: {}".format(monster.id, monster.monster_name))

                user_input = input("\nType the number of the fighter you would like to add or [q] to back."
                                   "\n>> ").lower()

                if user_input == 'q':
                    break
                else:
                    try:
                        """Try and retrieve the monster's information based on the monster's id.
                        If it doesn't exist, then complain to the user. If it does exist, then add
                        that monster, and subtract a line from the screen"""

                        monster = Monsters.get(Monsters.id == user_input)
                        battle_list.append({"name": monster.monster_name, "player": False,
                                            "init": monster.init_mod, "turn": False})
                    except Monsters.MonstersDoesNotExist:
                        print(Fore.RED + "** Invalid entry. That monster does not exist")
                    else:
                        self.lines -= 1
                        break

    def battle(self):
        """Commence the battle. Loop through each player to let the user
        know who's turn it currently is. Keep looping until the battle is over."""

        battle_over = False

        # Main battle loop
        while True:
            i = 0

            """Loop through all of the players to let the user know who's turn it is.
            The battle_list length must be recalculated every time because the length
            of the list changes."""
            while i < len(battle_list):

                # Set the previous fighter's turn to False if they aren't the first on the battle_list
                try:
                    battle_list[i - 1]['turn'] = False
                except IndexError:
                    pass

                # Set the current fighter's turn to True
                battle_list[i]['turn'] = True
                user_input = self.print_screen(self.lines, options="Enter [d] to mark a player as Dead, [q] to quit, or"
                                                                   " <enter> for the next player's turn\n>> ").lower()
                if user_input == 'd':
                    self.remove_fighter()
                    continue
                elif user_input == 'q':
                    battle_over = True
                    break
                else:
                    i += 1

            if battle_over:
                break

    def remove_fighter(self):
        """Remove a fighter from the current battle list"""

        try:
            user_input = int(self.print_screen(self.lines, options="Who was taken out "
                                                                   "of combat?\n>> ", show_numbers=True))
        except ValueError:
            pass
        else:
            try:
                del battle_list[user_input - 1]
                self.lines += 1
            except IndexError:
                input("Fighter does not exist...")


def initialize_battle():
    """Initialize the fight."""

    # Create the screen object
    screen = Screen()

    # Main screen loop
    while True:
        user_input = screen.print_screen(screen.lines)

        if user_input == 'q':                                   # Return to the main menu
            break
        elif user_input == 'a':                                 # Add fighters to the battle list
            screen.add_fighters_to_battle_list()
        elif user_input == 'i':                                 # Initialize the fight

            if not battle_list:                                 # Give error if there are no fighters added
                input(Fore.RED + "** ERROR: No fighters added to current battle")
            else:

                # Roll all character's initiatives, sort the fighting order, and commence battle
                screen.roll_init()
                screen.reverse_bubble_sort_list()
                screen.battle()
