from container_strategy import Container


class Bowl(Container):
    @staticmethod
    def fill(board):
        board.itemAtPosition(4, 0).widget().set_blocking(True)
        board.itemAtPosition(4, 19).widget().set_blocking(True)
        board.itemAtPosition(5, 0).widget().set_blocking(True)
        board.itemAtPosition(5, 19).widget().set_blocking(True)

        j_left = 1
        j_right = 18

        for i in range(6, 13):
            board.itemAtPosition(i, j_left).widget().set_blocking(True)
            board.itemAtPosition(i, j_right).widget().set_blocking(True)

            j_left += 1
            j_right -= 1

        for i in range(8, 12):
            board.itemAtPosition(13, i).widget().set_blocking(True)
