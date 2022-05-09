from PyQt5.QtWidgets import QLabel


class Tile(QLabel):
    taken_stylesheet = "Tile{\n" \
        "border: 1px solid black;\n" \
        "background-color: rgb(255, 178, 102);\n" \
        "}"
    no_blocking_stylesheet = "Tile{\n" \
        "border: 1px solid black;\n" \
        "background-color: rgb(255, 255, 255);\n" \
        "}"
    blocking_stylesheet = "Tile{\n" \
        "border: 1px solid black;\n" \
        "background-color: rgb(32, 32, 32);\n" \
        "}"

    def __init__(self, blocking: bool = False, sand: bool = False):
        super(Tile, self,).__init__()
        self.sand = sand
        self.blocking = blocking
        self.setFixedWidth(40)
        self.setFixedHeight(40)

        if self.blocking:
            self.setStyleSheet(self.blocking_stylesheet)
        elif not self.blocking:
            self.setStyleSheet(self.no_blocking_stylesheet)
        elif self.sand:
            self.setStyleSheet(self.taken_stylesheet)

    def is_blocking(self):
        return self.blocking

    def set_blocking(self, blocking):
        self.blocking = blocking

        if not self.blocking:
            self.setStyleSheet(self.no_blocking_stylesheet)
        else:
            self.setStyleSheet(self.blocking_stylesheet)

    def set_sand(self, sand=True):
        self.sand = sand
        if self.sand:
            self.blocking = True
            self.setStyleSheet(self.taken_stylesheet)
        else:
            self.blocking = False
            self.setStyleSheet(self.no_blocking_stylesheet)

    def is_sand(self):
        return self.sand
