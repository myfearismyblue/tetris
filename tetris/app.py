from os import name, system
from threading import Thread
from time import sleep
from typing import List

from pynput import keyboard

from container import movement_manager
from physics import IMovementManager
from preset_figures import *
import config as cfg
from services.keyboard_handlers import KeyboardHandlers


class ClassicalApp:
    def __init__(self, movement_manager: IMovementManager):
        self._movement_manager = movement_manager
        figures = [dash_figure, L_figure, square_figure, Z_figure, S_figure, back_L_figure,  T_figure]
        self._movement_manager.set_available_figures(figures)
        self._keyboard_handlers = KeyboardHandlers(movement_manager=self._movement_manager)
        self._listener = keyboard.Listener(on_press=self._keyboard_handlers.on_press)
        self.score = 0

    @staticmethod
    def _clear_screen():
        """Auxiliary func to clear terminal's screen"""
        # for windows
        if name == 'nt':
            _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')

    def _keyboard_handling_loop(self):
        with self._listener:  # starting keyboard event handling loop
            self._listener.join()

    def _physics_mainloop(self):
        self._movement_manager.start_game()
        while self._movement_manager.game_is_alive:
            self._movement_manager.tick_game()

    def _graphics_mainloop(self):
        while self._movement_manager.game_is_alive:
            sleep(1 / cfg.GRAPHICS_FRAME_RATE)
            self._count_and_update_score()
            self._clear_screen()
            print(self._movement_manager)
        self._clear_screen()
        print(f'Game is over. Your score: {self.score:.0f}')

    def start(self):
        physics_loop = Thread(target=self._physics_mainloop)
        keyboard_loop = Thread(target=self._keyboard_handling_loop)
        keyboard_loop.daemon = True
        graphics_loop = Thread(target=self._graphics_mainloop)
        keyboard_loop.start()
        graphics_loop.start()
        physics_loop.start()

    def _count_and_update_score(self):
        addition = 0
        moves: List[List[int]] = self._movement_manager.pop_scored_lines()
        for combo in moves:
            for item in combo:
                addition += 100 * item * item / 2
        self.score += addition


def main():
    tet = ClassicalApp(movement_manager=movement_manager)
    tet.start()


if __name__ == '__main__':
    main()
