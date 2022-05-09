import time

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from square_checker import SquareChecker


class SimulationThread(QThread):
    changes_detected = True
    update_to_state = pyqtSignal(tuple, int)
    single_drop = pyqtSignal(int, int)

    def __init__(self, client, parent=None):
        QThread.__init__(self, parent)
        self.square_checker = SquareChecker(self, client)
        self.client = client
        self.pause = False
        self.turn_any_changes = False
        self.any_changes = True
        self.working = False

    def run(self):
        self.working = True
        self.any_changes = True
        self.turn_any_changes = False
        self.pause = False

        print("POCZATEK")
        while self.any_changes:
            if not self.pause:
                for square in self.client.from_00:
                    self.square_checker.check_square(square)
                    # time.sleep(0.001)

                self.turn_any_changes = False

                for square in self.client.from_11:
                    self.check_double_square(square[0][0])
                    self.square_checker.check_square(square)
                    # time.sleep(0.001)

                if not self.turn_any_changes:
                    self.any_changes = False

        self.pause = False
        self.working = False

        print("KONIEC")

    def stop(self):
        self.terminate()

    def check_square(self, square):
        sand = [self.client.board.itemAtPosition(
            x, y).widget().is_sand() for x, y in square]
        blocking = [self.client.board.itemAtPosition(
            x, y).widget().is_blocking() for x, y in square]

        if sand[0] and sand[1] and not blocking[2] and not blocking[3]:
            self.turn_any_changes = True
            self.update_to_state.emit(square, 5)

        elif sand[0] and sand[2] and not sand[1] and not blocking[3]:
            self.turn_any_changes = True
            self.update_to_state.emit(square, 3)

        elif sand[1] and sand[3] and not sand[0] and not blocking[2]:
            self.turn_any_changes = True
            self.update_to_state.emit(square, 4)

        elif sand[0] and not blocking[2]:
            self.turn_any_changes = True
            self.update_to_state.emit(square, 1)

        elif sand[1] and not blocking[3]:
            self.turn_any_changes = True
            self.update_to_state.emit(square, 2)

    def check_double_square(self, x):
        if self.client.board.itemAtPosition(x, 0).widget().is_sand() and not self.client.board.itemAtPosition(x+1, 0).widget().is_blocking():
            self.single_drop.emit(x, 0)

        if self.client.board.itemAtPosition(x, 19).widget().is_sand() and not self.client.board.itemAtPosition(x+1, 19).widget().is_blocking():
            self.single_drop.emit(x, 19)
