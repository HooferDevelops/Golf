"""
    Golf Game
    4/4/2022 - 
"""

try:
    import pygame
    print("module 'pygame' is installed")
except ModuleNotFoundError:
    import pip
    print("module 'pygame' is not installed")
    pip.main(['install', 'pygame'])
    print("Restart the application to continue")
    exit()

import content.game as game

# start game
golf = game.Golf()
golf.gameLoop()