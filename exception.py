class OutOfBoardError(Exception):
    def __init__ (self,x,y):
        super().__init__(f"toa do {(x,y)} o ngoai ban do")
class AlreadyShotError(Exception):
    def __init__(self, x, y):
        super().__init__(f"Da ban vao toa do {(x, y)}")
