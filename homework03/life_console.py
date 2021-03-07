import curses
import time

import pygame

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)
        # self.screen = pygame.display.set_mode((self.life.rows,self.life.cols))


    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        horizontal_border = '+' + ("-" * (self.life.cols)) + ("+")
        screen.addstr(horizontal_border)
        # print(horizontal_border)
        for i in range(1, self.life.rows):
            central_string = "|" + (" " * (self.life.cols)) + ("|")
            screen.addstr(i, 0, central_string)
            # print(central_string)
        # print(horizontal_border)
        screen.addstr(self.life.rows, 0, horizontal_border)
        # screen.refresh()

    def draw_grid(self, screen) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        # screen.addstr(0, 0, "dffffffffffffffff", curses.color_pair(1))
        play_screen = []
        for i in range(self.life.rows-1):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    screen.addstr(i+1, j+1, "*")

    def run(self) -> None:
        # pygame.init()
        #
        # pygame.display.set_caption("Game of Life")
        # self.screen.fill(pygame.Color("white"))
        screen = curses.initscr()
        screen.nodelay(True)
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)
        # win = curses.newwin(self.life.rows + 10, self.life.cols + 10)
        # screen.refresh()
        # curses.start_color()
        # PUT YOUR CODE HERE
        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            time.sleep(0.2  )
            self.life.step()
            screen.clear()

        curses.endwin()


# def draw(canvas):
#     row, column = (5, 20)
#     canvas.addstr(row, column, 'Hello, World!')
#     canvas.refresh()
#     time.sleep(1)


if __name__ == '__main__':
    life = GameOfLife((24, 80), max_generations=50)
    ui = Console(life)
    ui.run()
