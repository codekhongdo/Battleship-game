import numpy as np
from ship import *
from exception import *
class Board:
    def __init__(self):
        self.grid=np.zeros((10,10),dtype=int)
        self.__ships=[]
        self.shots=set()
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
        if not (0 <= x < 10 and 0 <= y < 10):
            raise OutOfBoardError(x,y)
        if (x,y) in self.shots:
            raise AlreadyShotError(x,y)
        self.shots.add((x,y))
        for ship in self.__ships:
            if (x, y) in ship.get_positions():
                ship.hits += 1
                self.grid[y][x] = 3
                if ship.isSunk():
                    print("tàu bị chìm")
                return "HIT"
        self.grid[y][x] = 2
        return "MISS"
    def check_lose(self):
        return all(i.isSunk() for i in self.__ships)
