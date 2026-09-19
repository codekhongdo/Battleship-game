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

