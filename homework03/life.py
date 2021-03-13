import math
import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
            self,
            size: tp.Tuple[int, int],
            randomize: bool = True
    ) -> None:
        # Размер клеточного поля
        self.max_generations = math.inf
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        # self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

        # Создание нового окна

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
        for i in range(self.rows):
            cell_string = []
            for j in range(self.cols):
                if randomize:
                    number = random.randint(0, 1)
                else:
                    number = 0
                # print(number)
                cell_string.append(number)
            cell_grid.append(cell_string)
        # print(cell_grid)
        return cell_grid

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
            if i < 0 or i >= self.rows:
                continue
            for j in range(cell[1] - 1, cell[1] + 2):
                if j < 0 or j >= self.cols:
                    continue
                if i == cell[0] and j == cell[1]:
                    continue
                # print("i in get_neighbors(): " + str(i))
                # print("curr_generation size: " + str(len(self.curr_generation)))
                # print("j in get_neighbors(): " + str(j))
                # print("curr_generation[0] size: " + str(len(self.curr_generation[0])))
                # print("curr generation cell[i][j]: " + str(self.curr_generation[i][j]))
                neighbours.append(self.curr_generation[i][j])
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        grid = []
        for i in range(self.rows):
            grid_string = []
            for j in range(self.cols):
                neighbours = self.get_neighbours((i, j)).count(1)
                if neighbours < 2 or neighbours > 3:
                    cell = 0
                elif neighbours == 3:
                    cell = 1
                else:
                    cell = self.curr_generation[i][j]
                grid_string.append(cell)
            grid.append(grid_string)
        return grid

    def step(self) -> None:
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations = self.generations + 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """

        return self.generations > self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return not self.curr_generation.__eq__(self.prev_generation)

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        f = open(filename, 'r')

        grid = []
        i = 0
        for line in f:
            string = []
            for j in line:
                if not j == '\n':
                    string.append(int(j))
            grid.append(string)
        # grid=grid[:-1]
        # curr_generation = grid
        print('What was in file:')
        print(grid)
        print("Height of grid: " + str(len(grid)))
        print("Height of grid: " + str(len(grid[0])))
        temp = GameOfLife((len(grid), len(grid[0])), True)
        temp.curr_generation = grid
        return temp

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        f = open(filename, 'w')
        print("method save:")
        for i in self.curr_generation:
            string = ""
            for j in i:
                print("j=" + str(j))
                string += str(j)
            string += '\n'
            print("string which will be appended: " + string)
            f.write(str(string))
        # f.read()
        f.close()

# life1 = GameOfLife((5,5))
# life1 = GameOfLife.from_file(pathlib.Path('glider.txt'))
# print(life1.curr_generation)
# for k in range(4):
#     print("i=" + str(k))
#     life1.step()
#     print(life1.curr_generation)
# # print(life1.curr_generation)
# life1.save(pathlib.Path('glider-4-steps.txt'))
