
import pygame
from Document import Tools, setup
from Document.status import menu, load, level
from PlaneGame import PlaneGame

def main():

    state_dict = {
        'menu':menu.Menu(),
        'load':load.LoadScreen(),
        'level':level.Level(),
        'game_over':load.Game_Over(),
        'success':load.Success(),
        'plane_game':load.plane_game()
    }
    game = Tools.Game(state_dict, 'menu')
    # state = menu.Menu()
    # state = load.LoadScreen()
    state = level.Level()
    game.run()


if __name__ == '__main__':
    main()

    # PlaneGame().startGame()

