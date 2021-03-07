import random
import typing as tp

import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size

        # Устанавливаем размер окна
        self.screen_size = self.width, self.height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        # Скорость протекания игры
        self.speed = speed
        # self.grid = self.create_grid(randomize=True)

    def draw_lines(self) -> None:
        # Copy from previous assignment
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """

        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'),
                                     [j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size])
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'),
                                     [j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size])

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        # PUT YOUR CODE HERE
        run, pause = 0, 1
        status = pause
        position = []
        running = True
        # grid = GameOfLife.create_grid(self, True)
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL:
                        status = pause
                    if event.key == pygame.K_SPACE:
                        status = run
                if status == pause:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            position.append(event.pos)

            self.draw_grid()
            self.draw_lines()
            if status == pause:
                if not (position == []):
                    for pos in position:
                        a = pos[0] // self.cell_size
                        b = pos[1] // self.cell_size
                        if self.life.curr_generation[b][a] == 0:
                            self.life.curr_generation[b][a] = 1
                        else:
                            self.life.curr_generation[b][a] = 0
                    self.draw_grid()
                    self.draw_lines()
                    position = []
            else:
                self.life.step()
            if (not self.life.is_changing) or self.life.is_max_generations_exceeded:
                running = False
            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    game = GameOfLife((50, 70), randomize=True)
    # Grid = game.create_grid(True)
    # print("After: ", Grid)

    gui = GUI(game, speed=30)
    gui.run()
