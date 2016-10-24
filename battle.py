import random
import main

from colorama import Fore, Back, Style, init

current_fighters = []


def initialize_battle():
    """Initialize the fight."""
    for fighter in current_fighters:
        print(fighter.fighter_name)
    input(">> ")