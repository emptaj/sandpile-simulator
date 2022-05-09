from os import sys
from functools import partial

from qt_material import apply_stylesheet

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from tile import Tile
from container_strategy import Bowl, Circle, Lines, SandGlass
import random

import time

class SimulationThread(QThread):
    changes_detected = True
    update_to_state = pyqtSignal(tuple, int)
    single_drop = pyqtSignal(int, int)

    def __init__(self, client, parent=None):
        QThread.__init__(self, parent)
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

        while self.any_changes:
            if not self.pause:
                for square in self.client.from_00:
                    self.check_square(square)
                    time.sleep(0.001)
                
                self.turn_any_changes = False

                for square in self.client.from_11:
                    self.check_double_square(square[0][0])
                    self.check_square(square)
                    time.sleep(0.001)

                if not self.turn_any_changes:
                    self.any_changes = False

                
        self.pause = False
        self.working = False
        

    def stop(self):
        self.terminate()

    def check_square(self, square):
        sand = [self.client.board.itemAtPosition(x, y).widget().is_sand() for x,y in square]
        blocking = [self.client.board.itemAtPosition(x, y).widget().is_blocking() for x,y in square]

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
        
                

class GUIApp(QMainWindow):
    def __init__(self):
        super(GUIApp, self).__init__()
        self.text = "Siema"
        uic.loadUi("stylesheet.ui", self)

        self.connect_btns()
        self.setWindowTitle("Symulator opadania piasku")
        self.make_board()
        self.from_00 = []
        self.from_11 = []
        self.make_sub_grids()
        self.initialize_board()
        self.setFixedSize(1228, 670)
        self.show()

    def connect_btns(self):
        self.worker = SimulationThread(self)
        self.sand_container1.clicked.connect(partial(self.select_sand_container, Lines()))
        self.sand_container2.clicked.connect(partial(self.select_sand_container, Circle()))
        self.sand_container3.clicked.connect(partial(self.select_sand_container, Bowl()))
        self.sand_container4.clicked.connect(partial(self.select_sand_container, SandGlass()))
        self.clear_btn.clicked.connect(self.initialize_board)
        
        self.generate_sand_btn.clicked.connect(partial(self.generate_sand, False))
        self.generate_sand_rnd_btn.clicked.connect(partial(self.generate_sand, True))

        self.start_btn.clicked.connect(self.start_simulation)
        self.stop_btn.clicked.connect(self.stop_simulation)
        
        self.label.setProperty('class', 'warning')
        self.label_2.setProperty('class', 'warning')
        
        self.start_btn.setProperty('class', 'success')
        self.stop_btn.setProperty('class', 'warning')

        self.worker.update_to_state.connect(self.update_square)
        self.worker.single_drop.connect(self.drop)


    def update_square(self, square, new_state):
        if new_state == 1:
            self.board.itemAtPosition(square[0][0], square[0][1]).widget().set_sand(False)
            self.board.itemAtPosition(square[2][0], square[2][1]).widget().set_sand(True)

        elif new_state == 2:
            self.board.itemAtPosition(square[1][0], square[1][1]).widget().set_sand(False)
            self.board.itemAtPosition(square[3][0], square[3][1]).widget().set_sand(True)

        elif new_state == 3:
            self.board.itemAtPosition(square[0][0], square[0][1]).widget().set_sand(False)
            self.board.itemAtPosition(square[3][0], square[3][1]).widget().set_sand(True)

        elif new_state == 4:
            self.board.itemAtPosition(square[1][0], square[1][1]).widget().set_sand(False)
            self.board.itemAtPosition(square[2][0], square[2][1]).widget().set_sand(True)

        elif new_state == 5:
            self.board.itemAtPosition(square[0][0], square[0][1]).widget().set_sand(False)
            self.board.itemAtPosition(square[1][0], square[1][1]).widget().set_sand(False)

            self.board.itemAtPosition(square[2][0], square[2][1]).widget().set_sand(True)
            self.board.itemAtPosition(square[3][0], square[3][1]).widget().set_sand(True)

    def drop(self, x, y):
        self.board.itemAtPosition(x, y).widget().set_sand(False)
        self.board.itemAtPosition(x+1, y).widget().set_sand(True)


    def start_simulation(self): 
        if not self.worker.pause:
            self.worker.start()
        else:
            self.worker.pause = False
        
            
    def stop_simulation(self):
        if self.worker.working and not self.worker.pause:
            self.worker.pause = True

    def select_sand_container(self, strategy):
        self.initialize_board()
        strategy.fill(self)

    def make_board(self):
        for i in range(14):
            for j in range(20):
                self.board.addWidget(Tile(False), i, j)
        
    def initialize_board(self):
        for i in range(14):
            for j in range(20):
                if self.board.itemAtPosition(i, j).widget().is_blocking():
                    self.board.itemAtPosition(i, j).widget().set_sand(False)
                    self.board.itemAtPosition(i, j).widget().set_blocking(False)
                    

    def make_sub_grids(self):
        rows = 14
        ceils = 20

        for i in range(0, rows-1, 2):
            for j in range(0, ceils-1, 2):
                square = ((i, j), (i, j+1),
                (i+1, j), (i+1, j+1))
                self.from_00.append(square)


        for i in range(1, rows-1, 2):
            for j in range(1, ceils-1, 2):
                square = ((i, j), (i, j+1),
                (i+1, j), (i+1, j+1))
                self.from_11.append(square)


    def generate_sand(self, generate_random = False):
        if generate_random:
            how_many = random.randint(10, 40)
            x = []
            y = []

            for _ in range(how_many):
                x.append(random.randint(0,2))
                y.append(random.randint(0, 19))   

            for cord_x, cord_y in zip(x, y):
                if not self.board.itemAtPosition(cord_x, cord_y).widget().is_blocking():
                    self.board.itemAtPosition(cord_x, cord_y).widget().set_sand()

        else:
            for i in range(0,20):
                self.board.itemAtPosition(0, i).widget().set_sand()
                self.board.itemAtPosition(1, i).widget().set_sand()

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