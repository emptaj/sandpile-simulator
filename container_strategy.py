from abc import ABC, abstractmethod


class Container(ABC):
    possible = None

    @abstractmethod
    def fill():
        pass
