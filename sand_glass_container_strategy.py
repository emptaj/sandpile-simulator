from container_strategy import Container


class SandGlass(Container):
    @staticmethod
    def fill(board):
        i = 2
        j_left = 2
        j_right = 17
        while i < 9:
            board.itemAtPosition(i, j_left).widget().set_blocking(True)
            board.itemAtPosition(i, j_right).widget().set_blocking(True)
            j_left += 1
            j_right -= 1
            i += 1

        j_left = 7
        j_right = 12
        while i < 14:
            board.itemAtPosition(i, j_left).widget().set_blocking(True)
            board.itemAtPosition(i, j_right).widget().set_blocking(True)
            j_left -= 1
            j_right += 1
            i += 1

        for i in range(2, 18):
            board.itemAtPosition(13, i).widget().set_blocking(True)
