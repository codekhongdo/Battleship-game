from Battleship_class import*
name=input("nhập tên của bạn: ")
Player1=Human(name)
Player2=EasyAI("máy")
Player3=HardAI("máy")
ship1=Ship(3)
ship2=Ship(3)
ship3=Ship(3)
Player1.board.place_ship(ship1, 0, 0, 'H')
Player2.board.place_ship(ship2, 2, 3, 'V')
Player3.board.place_ship(ship3,2,3,'V')
level=int(input("chọn chế độ 1.dễ/2.khó:"))
while True:
    if (level==1):
        x,y=Player1.takeShot()
        Player2.board.receive_shot(x,y)
        if Player2.board.check_lose():
            print("Bạn đã thắng!")
            break
        a,b=Player2.takeShot()
        Player1.board.receive_shot(a,b)
        if Player1.board.check_lose():
            print("Máy đã thắng")
            break
    if (level==2):
        x,y=Player1.takeShot()
        Player3.board.receive_shot(x,y)
        if Player3.board.check_lose():
            print("Bạn đã thắng!")
            break
        x,y=Player3.takeShot()
        ket_qua=Player1.board.receive_shot(x,y)
        Player3.afterShot(ket_qua)
        while len(Player3.targets) > 0:
            print(f"🔥 Máy đang nã combo đạn xung quanh!")
            x,y=Player3.takeShot()
            ket_qua_combo=Player1.board.receive_shot(x,y)
            Player3.afterShot(ket_qua_combo)
            if Player1.board.check_lose():
                print("Máy đã thắng")
                break
        if Player1.board.check_lose():
            break