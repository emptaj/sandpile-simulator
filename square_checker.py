from threading import Thread
from abc import ABC, abstractmethod


class SquareChecker():
    def __init__(self, simulation_thread, client) -> None:
        self.client = client
        self.simulation_thread = simulation_thread

    def check_square(self, square):
        sand = [self.client.board.itemAtPosition(
            x, y).widget().is_sand() for x, y in square]
        blocking = [self.client.board.itemAtPosition(
            x, y).widget().is_blocking() for x, y in square]

        if sand[0] and sand[1] and not blocking[2] and not blocking[3]:
            self.turn_any_changes = True
            self.simulation_thread.update_to_state.emit(square, 5)

        elif sand[0] and sand[2] and not sand[1] and not blocking[3]:
            self.turn_any_changes = True
            self.simulation_thread.update_to_state.emit(square, 3)

        elif sand[1] and sand[3] and not sand[0] and not blocking[2]:
            self.turn_any_changes = True
            self.simulation_thread.update_to_state.emit(square, 4)

        elif sand[0] and not blocking[2]:
            self.turn_any_changes = True
            self.simulation_thread.update_to_state.emit(square, 1)

        elif sand[1] and not blocking[3]:
            self.turn_any_changes = True
            self.simulation_thread.update_to_state.emit(square, 2)

    def check_double_square(self, x):
        if self.client.board.itemAtPosition(x, 0).widget().is_sand() and not self.client.board.itemAtPosition(x+1, 0).widget().is_blocking():
            self.simulation_thread.single_drop.emit(x, 0)

        if self.client.board.itemAtPosition(x, 19).widget().is_sand() and not self.client.board.itemAtPosition(x+1, 19).widget().is_blocking():
            self.simulation_thread.single_drop.emit(x, 19)
