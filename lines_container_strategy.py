from container_strategy import Container


class Lines(Container):
    @staticmethod
    def fill(board):
        taken = [
            (2, 2),
            (3, 3),
            (4, 4),
            (7, 10),
            (8, 11),
            (9, 12),
            (10, 13),
            (4, 7),
            (5, 6),
            (6, 5),
            (7, 4),
            (4, 14),
            (3, 15),
            (2, 16),
        ]
        for i in range(20):
            board.itemAtPosition(13, i).widget().set_blocking(True)

        for position in taken:
            board.itemAtPosition(
                position[0], position[1]).widget().set_blocking(True)
