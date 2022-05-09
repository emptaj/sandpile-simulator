from abc import ABC, abstractmethod


class Container(ABC):
    possible = None

    @abstractmethod
    def fill():
        pass

class Bowl(Container):
    @staticmethod
    def fill(simulator):
        simulator.board.itemAtPosition(4, 0).widget().set_blocking(True)
        simulator.board.itemAtPosition(4, 19).widget().set_blocking(True)
        simulator.board.itemAtPosition(5, 0).widget().set_blocking(True)
        simulator.board.itemAtPosition(5, 19).widget().set_blocking(True)
        
        j_left = 1
        j_right = 18

        for i in range(6,13):
            simulator.board.itemAtPosition(i, j_left).widget().set_blocking(True)
            simulator.board.itemAtPosition(i, j_right).widget().set_blocking(True)
            
            j_left += 1
            j_right -= 1

        for i in range(8,12):
            simulator.board.itemAtPosition(13, i).widget().set_blocking(True)


class Lines(Container):
    @staticmethod
    def fill(simulator):
        taken = [
           (2,2),
           (3,3),
           (4,4),
           (7,10),
           (8,11),
           (9,12),
           (10,13),
           (4,7),
           (5,6),
           (6,5),
           (7,4),
           (4,14),
           (3,15),
           (2,16),
       ]
        for i in range(20):
            simulator.board.itemAtPosition(13, i).widget().set_blocking(True)
        
        for position in taken:
             simulator.board.itemAtPosition(position[0], position[1]).widget().set_blocking(True)

class SandGlass(Container):
    @staticmethod
    def fill(simulator):
        i = 2
        j_left = 2
        j_right = 17 
        while i < 9:
             simulator.board.itemAtPosition(i, j_left).widget().set_blocking(True)
             simulator.board.itemAtPosition(i, j_right).widget().set_blocking(True)
             j_left += 1
             j_right -= 1
             i += 1

        j_left = 7
        j_right = 12
        while i < 14:
            simulator.board.itemAtPosition(i, j_left).widget().set_blocking(True)
            simulator.board.itemAtPosition(i, j_right).widget().set_blocking(True)
            j_left -= 1
            j_right += 1
            i += 1
        
        for i in range(2,18):
             simulator.board.itemAtPosition(13, i).widget().set_blocking(True)

class Circle(Container):
    @staticmethod
    def fill(simulator):
        simulator.board.itemAtPosition(2, 9).widget().set_blocking(True)
        simulator.board.itemAtPosition(3, 8).widget().set_blocking(True)
        simulator.board.itemAtPosition(3, 10).widget().set_blocking(True)
        simulator.board.itemAtPosition(3, 7).widget().set_blocking(True)
        simulator.board.itemAtPosition(3, 11).widget().set_blocking(True)
        simulator.board.itemAtPosition(4, 6).widget().set_blocking(True)
        simulator.board.itemAtPosition(4, 12).widget().set_blocking(True)
        simulator.board.itemAtPosition(5, 5).widget().set_blocking(True)
        simulator.board.itemAtPosition(5, 13).widget().set_blocking(True)
        simulator.board.itemAtPosition(6, 5).widget().set_blocking(True)
        simulator.board.itemAtPosition(6, 13).widget().set_blocking(True)
        simulator.board.itemAtPosition(7, 6).widget().set_blocking(True)
        simulator.board.itemAtPosition(7, 12).widget().set_blocking(True)
        simulator.board.itemAtPosition(8, 7).widget().set_blocking(True)
        simulator.board.itemAtPosition(8, 8).widget().set_blocking(True)
        simulator.board.itemAtPosition(8, 11).widget().set_blocking(True)
        simulator.board.itemAtPosition(8, 10).widget().set_blocking(True)
        simulator.board.itemAtPosition(9, 9).widget().set_blocking(True)




