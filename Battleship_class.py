import numpy as np
import random
from abc import ABC,abstractmethod
from ship import *
from board import *
class Player(ABC):
    def __init__(self,name):
        self.name=name
        self.board=Board()
    @abstractmethod
    def takeShot(self, target_board):
        pass
class Human(Player):
    def __init__(self, name):
        super().__init__(name)
    def takeShot(self, target_board):
        while True:
            try:
                x,y=map(int,input("Nhap toa do (x,y)").split())
                Toa_do=(x,y)
                return Toa_do
            except ValueError:
                print("Lỗi định dạng! Hãy nhập 2 số nguyên, ví dụ: 2 4")
class EasyAI(Player):
    def __init__(self, name):
        super().__init__(name)
    def takeShot(self, target_board):
        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            coordinate = (x, y)
            if coordinate not in target_board.shots:
                return coordinate
class HardAI(Player):
    def __init__(self, name):
        super().__init__(name)
        self.targets=[]
        self.last_shot=None
    def takeShot(self, target_board):
        while True:
            if len(self.targets)>0:
                Toa_do=self.targets.pop()
                if Toa_do not in target_board.shots:
                    self.last_shot = Toa_do
                    return Toa_do
                continue
            x=random.randint(0,9)
            y=random.randint(0,9)
            Toa_do_HardAI=(x,y)
            if Toa_do_HardAI not in target_board.shots:
                self.last_shot = Toa_do_HardAI
                return Toa_do_HardAI
    def afterShot(self,ket_qua):
        if ket_qua=="HIT" and self.last_shot is not None:
            x, y = self.last_shot
            directions = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
            for nx,ny in directions:
                if 0 <= nx <= 9 and 0 <= ny <= 9:
                    if (nx, ny) not in self.targets:
                        self.targets.append((nx, ny))