import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
            self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:

        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed
        self.grid = self.create_grid(randomize=True)

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        # PUT YOUR CODE HERE

        running = True
        # grid = GameOfLife.create_grid(self, True)
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_lines()
            self.grid=self.get_next_generation()
            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        cell_grid = []
        for i in range(self.cell_height):
            cell_string = []
            for j in range(self.cell_width):
                if randomize:
                    number = random.randint(0, 1)
                else:
                    number = 0
                print(number)
                cell_string.append(number)
            cell_grid.append(cell_string)
        print(cell_grid)
        return cell_grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """

        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if self.grid[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'),
                                     [j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size])
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'),
                                     [j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size])

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        neighbours = []
        for i in range(cell[0] - 1, cell[0] + 2):
            if i < 0 or i >= self.cell_height:
                continue
            for j in range(cell[1] - 1, cell[1] + 2):
                if j < 0 or j >= self.cell_width:
                    continue
                if i == cell[0] and j == cell[1]:
                    continue
                neighbours.append(self.grid[i][j])
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        -----   -----
        out : Grid
            Новое поколение клеток.
        """
        grid=[]
        for i in range(self.cell_height):
            grid_string=[]
            for j in range(self.cell_width):
                neighbours=self.get_neighbours((i,j)).count(1)
                if neighbours<2 or neighbours>3:
                    cell=0
                elif neighbours==3:
                    cell=1
                else:
                    cell=self.grid[i][j]
                grid_string.append(cell)
            grid.append(grid_string)
        return grid




if __name__ == "__main__":
    game = GameOfLife(1920, 1080, 10)
    # Grid = game.create_grid(True)
    # print("After: ", Grid)
    game.run()
