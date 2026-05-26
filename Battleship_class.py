import numpy as np
import random
from abc import ABC,abstractmethod
class Ship:
    def __init__(self,size):
        self.size=size
        self.hits=0
        self.__positions=[]
    def get_positions(self):
        return self.__positions
    def isSunk(self):
        if (self.hits>=self.size):
            return True
        else:
            return False
class Board:
    def __init__(self):
        self.grid=np.zeros((10,10),dtype=int)
        self.__ships=[]
        self.shots=[]
    def print_board(self):
        for y in self.grid:
            print(y)
    def place_ship(self,ship,start_x,start_y,direction):
        list_potitions=[]
        if (direction=='S'):
            list_potitions.append((start_x, start_y))
            list_potitions.append((start_x + 1, start_y))
            list_potitions.append((start_x, start_y + 1))
            list_potitions.append((start_x + 1, start_y + 1))
        for i in range(ship.size):
            if (direction=='H'):
                list_potitions.append((start_x+i,start_y))
            if (direction=='V'):
                list_potitions.append((start_x,start_y+i))
        for x,y in list_potitions:
            if (direction == 'S') and (start_x>8 or start_y>8):
                return False
            if (x < 0 or x >= 10 or y < 0 or y >= 10):
                print("lỗi:tàu bị lòi ra ngoài bàn cờ")
                return False
            if self.grid[y][x]==1:
                print("lỗi:Vị trí này đã có tàu khác")
                return False
        for x,y in list_potitions:
            self.grid[y][x]=1
            ship.get_positions().append((x,y))
        self.__ships.append(ship)
        return True
    def receive_shot(self,x,y):
        hit_anything = False
        for ship in self.__ships:
            for a,b in ship.get_positions():
                if (x==a) and (y==b):
                    ship.hits+=1
                    self.grid[y][x]=3
                    hit_anything=True
                    if ship.isSunk():
                        print("tàu bị chìm")
                        return "HIT"
                    return "HIT"
            if hit_anything:
                break
        if not hit_anything:
            self.grid[y][x] = 2
            return "MISS"
    def check_lose(self):
        return all(i.isSunk() for i in self.__ships)
class Player(ABC):
    def __init__(self,name):
        self.name=name
        self.board=Board()
    @abstractmethod
    def takeShot(self):
        pass
class Human(Player):
    def __init__(self, name):
        super().__init__(name)
        self.shoted=[]
    def takeShot(self):
        while True:
            try:
                x,y=map(int,input("Nhap toa do (x,y)").split())
                if not (0<=x<=9 and 0<=y<=9):
                    print("Tọa độ phải từ 0 đến 9. Vui lòng nhập lại!")
                    continue
                Toa_do=(x,y)
                if Toa_do in self.shoted:
                    print("Ô này bạn đã bắn rồi! Hãy chọn ô khác.")
                    continue
                self.shoted.append(Toa_do)
                return Toa_do
            except ValueError:
                print("Lỗi định dạng! Hãy nhập 2 số nguyên, ví dụ: 2 4")
class EasyAI(Player):
    def __init__(self, name):
        super().__init__(name)
        self.spent_shots=[]
    def takeShot(self):
        while True:
            x=random.randint(0,9)
            y=random.randint(0,9)
            Toa_do_AI=(x,y)
            if Toa_do_AI not in self.spent_shots:
                self.spent_shots.append(Toa_do_AI)
                return Toa_do_AI
class HardAI(Player):
    def __init__(self, name):
        super().__init__(name)
        self.hard_shoted=[]
        self.targets=[]
    def takeShot(self):
        while True:
            if len(self.targets)>0:
                Toa_do=self.targets.pop()
                if Toa_do not in self.hard_shoted:
                    self.hard_shoted.append(Toa_do)
                    return Toa_do
                continue
            x=random.randint(0,9)
            y=random.randint(0,9)
            Toa_do_HardAI=(x,y)
            if Toa_do_HardAI not in self.hard_shoted:
                self.hard_shoted.append(Toa_do_HardAI)
                return Toa_do_HardAI
    def afterShot(self,ket_qua):
        if ket_qua=="HIT":
            x, y = self.hard_shoted[-1]
            directions = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
            for nx,ny in directions:
                if 0 <= nx <= 9 and 0 <= ny <= 9:
                    if (nx, ny) not in self.hard_shoted and (nx, ny) not in self.targets:
                        self.targets.append((nx, ny))