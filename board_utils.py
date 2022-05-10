
import random
from tile import Tile


class BoardUtils:
    @staticmethod
    def initialize_board(board):
        for i in range(14):
            for j in range(20):
                if board.itemAtPosition(i, j).widget().is_blocking():
                    board.itemAtPosition(i, j).widget().set_sand(False)
                    board.itemAtPosition(
                        i, j).widget().set_blocking(False)

    @staticmethod
    def make_board(board):
        for i in range(14):
            for j in range(20):
                board.addWidget(Tile(False), i, j)

    @staticmethod
    def generate_sand(client, generate_random=False):
        client.board_update_mutex.lock()

        if generate_random:
            count = random.randint(10, 40)
            x = []
            y = []

            for _ in range(count):
                x.append(random.randint(0, 2))
                y.append(random.randint(0, 19))

            for cord_x, cord_y in zip(x, y):
                if not client.board.itemAtPosition(cord_x, cord_y).widget().is_blocking():
                    client.board.itemAtPosition(
                        cord_x, cord_y).widget().set_sand()

        else:
            for i in range(0, 20):
                client.board.itemAtPosition(0, i).widget().set_sand()
                client.board.itemAtPosition(1, i).widget().set_sand()

        client.board_update_mutex.unlock()

    @classmethod
    def set_sand_container(cls, client, container_strategy):
        client.board_update_mutex.lock()
        cls.initialize_board(client.board)
        container_strategy.fill(client.board)
        client.board_update_mutex.unlock()

    @staticmethod
    def make_grids_from_squares(from_00, from_11):
        rows = 14
        ceils = 20

        for i in range(0, rows-1, 2):
            for j in range(0, ceils-1, 2):
                square = ((i, j), (i, j+1),
                          (i+1, j), (i+1, j+1))
                from_00.append(square)

        for i in range(1, rows-1, 2):
            for j in range(1, ceils-1, 2):
                square = ((i, j), (i, j+1),
                          (i+1, j), (i+1, j+1))
                from_11.append(square)

    @staticmethod
    def update_square(board, square, new_state):
        if new_state == 1:
            board.itemAtPosition(
                square[0][0], square[0][1]).widget().set_sand(False)
            board.itemAtPosition(
                square[2][0], square[2][1]).widget().set_sand(True)
        elif new_state == 2:
            board.itemAtPosition(
                square[1][0], square[1][1]).widget().set_sand(False)
            board.itemAtPosition(
                square[3][0], square[3][1]).widget().set_sand(True)
        elif new_state == 3:
            board.itemAtPosition(
                square[0][0], square[0][1]).widget().set_sand(False)
            board.itemAtPosition(
                square[3][0], square[3][1]).widget().set_sand(True)
        elif new_state == 4:
            board.itemAtPosition(
                square[1][0], square[1][1]).widget().set_sand(False)
            board.itemAtPosition(
                square[2][0], square[2][1]).widget().set_sand(True)

        elif new_state == 5:
            board.itemAtPosition(
                square[0][0], square[0][1]).widget().set_sand(False)
            board.itemAtPosition(
                square[1][0], square[1][1]).widget().set_sand(False)

            board.itemAtPosition(
                square[2][0], square[2][1]).widget().set_sand(True)
            board.itemAtPosition(
                square[3][0], square[3][1]).widget().set_sand(True)

    @staticmethod
    def drop_square(board, x, y):
        board.itemAtPosition(x, y).widget().set_sand(False)
        board.itemAtPosition(x+1, y).widget().set_sand(True)
