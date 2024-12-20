import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

class LogDisplay(tk.Frame):
    def __init__(self, master, logger):
        super().__init__(master)
        self.logger = logger  # Tham chiếu đến đối tượng Logger
        
        # Tạo ScrolledText để hiển thị log
        self.log_display = scrolledtext.ScrolledText(self, width=60, height=5, wrap=tk.WORD, state=tk.DISABLED)
        self.log_display.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Đọc log từ tệp và hiển thị trong GUI
        self.load_logs()

    def load_logs(self):
        """Đọc log từ tệp và chỉ hiển thị 3 dòng mới nhất từ trên xuống"""
        try:
            with open(self.logger.log_file, "r", encoding="utf-8") as file:
                log_content = file.readlines()  # Đọc tất cả dòng trong tệp
                last_3_logs = log_content[-5:]  # Lấy 3 dòng cuối cùng

                # Đảo ngược thứ tự các dòng log để log mới nhất hiển thị ở trên cùng
                last_3_logs.reverse()  # Đảo ngược danh sách dòng log

                # Chèn 3 dòng cuối vào phần hiển thị
                self.log_display.config(state=tk.NORMAL)
                self.log_display.delete("1.0", tk.END)  # Xóa toàn bộ nội dung
                self.log_display.insert(tk.END, ''.join(last_3_logs))  # Chèn 3 dòng mới nhất vào cuối
                self.log_display.config(state=tk.DISABLED)
        except FileNotFoundError:
            # Nếu tệp log không tồn tại, chỉ hiển thị thông báo rỗng
            pass

        
    def add_log(self, message):
        """Thêm log mới với timestamp"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{current_time}] {message}\n"
        
        # Thêm vào phần hiển thị log trong GUI, chèn vào đầu
        self.log_display.config(state=tk.NORMAL)
        self.log_display.insert("1.0", log_message)  # Chèn vào đầu
        self.log_display.config(state=tk.DISABLED)
        
        # Ghi log vào tệp thông qua Logger
        self.logger.add_log(log_message)

        # Giới hạn hiển thị chỉ 3 dòng mới nhất


class Logger:
    def __init__(self, log_file):
        self.log_file = log_file
        
    def add_log(self, message):
        """Ghi log vào tệp với mã hóa utf-8, mỗi lần chạy sẽ xóa nội dung tệp cũ"""
        with open(self.log_file, "a", encoding="utf-8") as file:  # Mở tệp với chế độ 'w' để ghi lại từ đầu
            file.write(message)

# Khởi tạo Logger và LogDisplay
logger = Logger("app_log.txt")  # Đảm bảo thư mục log tồn tại

