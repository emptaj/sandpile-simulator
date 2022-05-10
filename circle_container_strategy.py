from container_strategy import Container


class Circle(Container):
    @staticmethod
    def fill(board):
        board.itemAtPosition(2, 9).widget().set_blocking(True)
        board.itemAtPosition(3, 8).widget().set_blocking(True)
        board.itemAtPosition(3, 10).widget().set_blocking(True)
        board.itemAtPosition(3, 7).widget().set_blocking(True)
        board.itemAtPosition(3, 11).widget().set_blocking(True)
        board.itemAtPosition(4, 6).widget().set_blocking(True)
        board.itemAtPosition(4, 12).widget().set_blocking(True)
        board.itemAtPosition(5, 5).widget().set_blocking(True)
        board.itemAtPosition(5, 13).widget().set_blocking(True)
        board.itemAtPosition(6, 5).widget().set_blocking(True)
        board.itemAtPosition(6, 13).widget().set_blocking(True)
        board.itemAtPosition(7, 6).widget().set_blocking(True)
        board.itemAtPosition(7, 12).widget().set_blocking(True)
        board.itemAtPosition(8, 7).widget().set_blocking(True)
        board.itemAtPosition(8, 8).widget().set_blocking(True)
        board.itemAtPosition(8, 11).widget().set_blocking(True)
        board.itemAtPosition(8, 10).widget().set_blocking(True)
        board.itemAtPosition(9, 9).widget().set_blocking(True)
