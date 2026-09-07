class ship:
    def __init__(self,size):
        self.size=size
        self.hits=0
        self.__positions=[]
    def get_positions(self):
        return self.__positions
    def isSunk():
        if (self.hits>=self.size):
            return true
        else:
            return false

