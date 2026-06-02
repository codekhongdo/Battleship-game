# 🚢 BÁO CÁO KỸ THUẬT: BATTLESHIP 2D ENGINE
**Đề tài:** Ứng dụng Lập trình Hướng đối tượng (OOP) và Thuật toán dò tìm xây dựng Game Hải chiến.  
**Môn học:** Lập trình Hướng Đối Tượng  
**Đơn vị thực hiện:** Nhóm BETA  

---

## 👥 1. ĐỘI NGŨ PHÁT TRIỂN (NHÓM BETA)
Dự án được phân rã module theo đúng chuẩn quy trình phát triển phần mềm, với vai trò cụ thể của từng thành viên:
* 👨‍💻 Nguyễn Quang Thịnh (Nhóm trưởng)
* 🧠 Bùi Phan Anh (Thành viên)
* 💾 Bùi Thế Anh (Thành viên)
* 🎨 Nguyễn Việt Cường (Thành viên)

---

## 🎮 2. TỔNG QUAN LUẬT CHƠI & ĐIỂM SÁNG TẠO
**Battleship** là tựa game chiến thuật đánh theo lượt (Turn-based) giữa Người và Máy (AI).
* **Môi trường:** 2 lưới ma trận $10 \times 10$ ẩn/hiện song song (Cơ chế Sương mù chiến tranh).
* **Điểm sáng tạo cốt lõi:** Thay vì chỉ có các tàu đặt thẳng (Ngang/Dọc) như game truyền thống, nhóm đã lập trình thêm **Tàu đặc biệt hình khối vuông $2 \times 2$ (Square Ship)**, đòi hỏi thuật toán kiểm tra va chạm không gian (Collision Check) phức tạp hơn.
* **Mục tiêu:** Nã đạn dựa trên suy luận logic để bắn chìm toàn bộ 5 tàu của đối phương.

---

## ⚙️ 3. HỆ SINH THÁI CÔNG NGHỆ (TECH STACK)
Thay vì dùng Engine game có sẵn (Unity/Unreal), nhóm tự tay xây dựng hệ thống từ đầu bằng ngôn ngữ Python:
1. **Python 3.x:** Ngôn ngữ cốt lõi, áp dụng module `abc` để thiết kế Interface/Abstract Class.
2. **Pygame & Pygame.Mixer:** Xử lý đồ họa Render 60 FPS, bắt sự kiện chuột không đồng bộ và trộn âm thanh Stereo (Nhạc nền chạy độc lập với tiếng cháy nổ).
3. **NumPy:** **(Điểm nhấn kỹ thuật)** Số hóa vùng biển bằng ma trận `numpy.zeros((10,10), dtype=int)`. Việc ép kiểu số nguyên tĩnh giúp tốc độ truy xuất và tính toán của AI nhanh gấp 10 lần so với List lồng nhau thông thường của Python.

---

## 🏗️ 4. KIẾN TRÚC LẬP TRÌNH HƯỚNG ĐỐI TƯỢNG (OOP)
Mã nguồn được tổ chức chặt chẽ, thể hiện đầy đủ 4 tính chất của OOP:

### Tính Đóng gói (Encapsulation)
Các dữ liệu nhạy cảm được bảo vệ tuyệt đối khỏi file đồ họa (GUI) bên ngoài. 
* Ví dụ: Vị trí con tàu `__positions` trong class `Ship` hay danh sách tàu `__ships` trong class `Board` được đặt là **Private**. Chỉ có thể đọc thông qua hàm Getter `get_positions()`.

### Tính Trừu tượng (Abstraction)
Sử dụng thư viện `abc` tạo ra khuôn mẫu cho mọi thực thể tham gia trò chơi.
```python
class Player(ABC):
    def __init__(self, name):
        self.name = name
        self.board = Board()
    
    @abstractmethod
    def takeShot(self): pass 
```
---

### Tính Kế thừa & Đa hình (Inheritance & Polymorphism)
Các lớp Human, EasyAI, và HardAI đồng loạt Kế thừa từ lớp cha Player thông qua cú pháp khai báo lớp con trong Python.
```python
class EasyAI(Player):
    def __init__(self, name):
        super().__init__(name)   
        self.spent_shots = []

class HardAI(Player):
    def __init__(self, name):
        super().__init__(name)  
        self.hard_shoted = []
        self.targets = []
```
Tuy nhiên, các lớp con này thể hiện tính Đa hình bằng cách viết đè (Override) cùng một phương thức `takeShot()` nhưng xử lý logic hoàn toàn khác nhau:
* `Human`: Đợi tọa độ click từ chuột.
* `EasyAI`: Random tọa độ ngẫu nhiên.
* `HardAI`: Kích hoạt thuật toán dò tìm thông minh.

---

## 🧠 5. BỘ NÃO TRÍ TUỆ NHÂN TẠO (HARD AI ENGINE)
Để tạo độ khó cho game, nhóm phát triển thuật toán Cross-Search (Săn lùng chữ thập) kết hợp cấu trúc dữ liệu Ngăn xếp (Stack) cho lớp `HardAI`:
1. **Hunt Mode (Dò tìm):** Khi `self.targets` rỗng, máy bắn ngẫu nhiên để dò dấu vết.
2. **Target Mode (Săn lùng):** Ngay khi bắn trúng (`HIT`), hàm `afterShot()` kích hoạt. Thuật toán tự động tính toán 4 ô lân cận (Trên, Dưới, Trái, Phải), loại bỏ các ô tràn biên và đẩy vào Stack `self.targets`.
3. **Kết liễu:** Ở lượt sau, AI dùng lệnh `self.targets.pop()` rút tọa độ lân cận ra dồn ép bắn cho đến khi tàu địch chìm hoàn toàn.
```python
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
```
## 🖥️ 6. THUẬT TOÁN ĐỒ HỌA & QUẢN LÝ LUỒNG (GUI)
### Quản lý giao diện bằng Máy Trạng Thái (State Machine)
Để tránh xung đột luồng vẽ hình, game sử dụng 1 vòng lặp chính (Main Loop) được điều hướng bởi biến game_state đi qua 5 trạng thái:
`MENU` $\rightarrow$ `SETUP` (Đặt tàu) $\rightarrow$ `PLAYING` (Chiến đấu song song 2 bảng) $\rightarrow$ `GAME_OVER` $\rightarrow$ `HISTORY`.
### Thuật toán Ánh xạ Toán học (Pixel-to-Grid)
Hệ thống đồ họa (chuột) tính bằng Pixel, nhưng logic tính bằng ô Ma trận. Nhóm áp dụng công thức chia lấy phần nguyên để ánh xạ 2 chiều thời gian thực:
```python
grid_x=(mouse_x-MARGIN)//CELL_SIZE
grid_y=(mouse_y-MARGIN)//CELL_SIZE
```

---

## 💾 7. QUẢN LÝ DỮ LIỆU & LỊCH SỬ (FILE I/O)
* **Ghi dữ liệu**: Tại trạng thái `GAME_OVER`, hệ thống dùng thư viện datetime chụp mốc thời gian thực và ghi nối đuôi (Append) kết quả vào file `history.txt`.

* **Trực quan hóa (UX)**: Tại màn hình HISTORY, hệ thống dùng hàm `reversed()` để các trận đấu mới nhất luôn hiện lên đầu tiên. Cài đặt bộ lọc màu đồ họa: Chữ Xanh lá nếu chuỗi chứa từ "THẮNG", chữ Đỏ nếu chứa từ "THUA".

---

## 🚀 8. HƯỚNG DẪN KHỞI CHẠY (HOW TO RUN)
**Yêu cầu hệ thống:** Python 3.10+
**Cài đặt thư viện:**
``` bash
pip install pygame numpy
```
**Khởi chạy Giao diện chính:**
``` bash
python Battleship_gui.py
```
(Trò chơi cũng cung cấp file console_game.py nếu muốn kiểm thử logic tĩnh trên Terminal)
