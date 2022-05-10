from os import sys
from functools import partial

from qt_material import apply_stylesheet

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from board_utils import BoardUtils
from simulation import SimulationThread

from circle_container_strategy import Circle
from lines_container_strategy import Lines
from sand_glass_container_strategy import SandGlass
from bowl_container_strategy import Bowl


class GUIApp(QMainWindow):
    def __init__(self):
        super(GUIApp, self).__init__()
        self.text = "Siema"
        uic.loadUi("stylesheet.ui", self)

        self.board_update_mutex = QMutex()
        self.connect_btns()
        self.setWindowTitle("Symulator opadania piasku")
        BoardUtils.make_board(self.board)
        self.from_00 = []
        self.from_11 = []
        BoardUtils.make_grids_from_squares(self.from_00, self.from_11)
        BoardUtils.initialize_board(self.board)
        self.setFixedSize(1228, 670)
        self.show()

    def connect_btns(self):
        self.worker = SimulationThread(
            self)
        self.sand_container1.clicked.connect(
            partial(BoardUtils.set_sand_container, self, Lines()))
        self.sand_container2.clicked.connect(
            partial(BoardUtils.set_sand_container, self, Circle()))
        self.sand_container3.clicked.connect(
            partial(BoardUtils.set_sand_container, self, Bowl()))
        self.sand_container4.clicked.connect(
            partial(BoardUtils.set_sand_container, self, SandGlass()))
        self.clear_btn.clicked.connect(
            partial(BoardUtils.initialize_board, self.board))

        self.generate_sand_btn.clicked.connect(
            partial(BoardUtils.generate_sand, self, False))
        self.generate_sand_rnd_btn.clicked.connect(
            partial(BoardUtils.generate_sand, self, True))

        self.start_btn.clicked.connect(self.start_simulation)
        self.stop_btn.clicked.connect(self.stop_simulation)

        self.label.setProperty('class', 'warning')
        self.label_2.setProperty('class', 'warning')

        self.start_btn.setProperty('class', 'success')
        self.stop_btn.setProperty('class', 'warning')

        self.worker.update_to_state.connect(self.update_square)
        self.worker.single_drop.connect(self.drop_square)

    def update_square(self, square, new_state):
        self.board_update_mutex.lock()
        BoardUtils.update_square(self.board, square, new_state)
        self.board_update_mutex.unlock()

    def drop_square(self, x, y):
        self.board_update_mutex.lock()
        self.board.itemAtPosition(x, y).widget().set_sand(False)
        self.board.itemAtPosition(x+1, y).widget().set_sand(True)
        self.board_update_mutex.unlock()

    def start_simulation(self):
        if not self.worker.pause:
            self.worker.start()
        else:
            self.worker.pause = False

    def stop_simulation(self):
        if self.worker.working and not self.worker.pause:
            self.worker.pause = True


if __name__ == '__main__':
    app = QApplication(sys.argv)

    extra = {

        # Button colors
        'danger': '#dc3545',
        'warning': '#ffc107',
        # 'success2': '#17a2b8',
        'success':  '#38c219',

        # Font
        'font_family': 'Roboto',
        'font_size': '14px',
    }
    apply_stylesheet(app, theme='dark_red.xml', extra=extra)
    gui = GUIApp()
    sys.exit(app.exec_())
