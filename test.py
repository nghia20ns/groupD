import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

# Lớp Logger toàn cục
class GlobalLogger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.logs = []  # Danh sách log toàn cục
        return cls._instance

    def add_log(self, message):
        """Thêm log vào danh sách toàn cục"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{current_time}] {message}\n"
        self.logs.append(log_message)

    def get_logs(self, limit=None):
        """Lấy danh sách log, giới hạn số lượng nếu cần"""
        if limit:
            return self.logs[-limit:]  # Lấy số log mới nhất
        return self.logs  # Trả về toàn bộ log


# Lớp hiển thị log (Log Viewer)
class LogDisplay(tk.Frame):
    def __init__(self, master, logger, limit=None):
        super().__init__(master)
        self.logger = logger  # Tham chiếu đến Logger toàn cục
        self.limit = limit  # Số dòng log tối đa để hiển thị (None = tất cả)

        # Tạo ScrolledText để hiển thị log
        self.log_display = scrolledtext.ScrolledText(self, width=60, height=10, wrap=tk.WORD, state=tk.DISABLED)
        self.log_display.pack(fill="both", expand=True, padx=5, pady=5)

        # Tải log ban đầu
        self.load_logs()

    def load_logs(self):
        """Hiển thị log từ danh sách toàn cục"""
        logs = self.logger.get_logs(limit=self.limit)
        self.log_display.config(state=tk.NORMAL)
        self.log_display.delete("1.0", tk.END)
        self.log_display.insert("1.0", ''.join(reversed(logs)))  # Đảo log để log mới nhất ở trên cùng
        self.log_display.config(state=tk.DISABLED)

    def update_logs(self):
        """Cập nhật log mới khi có thay đổi"""
        self.load_logs()


# Tạo giao diện ứng dụng với nhiều trang
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.logger = GlobalLogger()  # Sử dụng Logger toàn cục
        self.title("Global Log Viewer")
        self.geometry("800x600")

        # Tạo container để quản lý các trang
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Dictionary lưu các trang
        self.frames = {}

        # Tạo các trang
        for F in (Page1, Page2, GlobalLogPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Hiển thị trang đầu tiên
        self.show_frame("Page1")

    def show_frame(self, page_name):
        """Hiển thị trang được chỉ định"""
        frame = self.frames[page_name]
        frame.tkraise()


# Trang 1
class Page1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Page 1", font=("Arial", 16))
        label.pack(pady=10)

        log_button = tk.Button(self, text="Add Log (Page 1)", command=self.add_log)
        log_button.pack(pady=5)

        next_page = tk.Button(self, text="Go to Page 2", command=lambda: controller.show_frame("Page2"))
        next_page.pack(pady=5)

        global_log_page = tk.Button(self, text="View Global Log", command=lambda: controller.show_frame("GlobalLogPage"))
        global_log_page.pack(pady=5)

    def add_log(self):
        """Thêm log từ trang 1"""
        self.controller.logger.add_log("Log added from Page 1")


# Trang 2
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Page 2", font=("Arial", 16))
        label.pack(pady=10)

        log_button = tk.Button(self, text="Add Log (Page 2)", command=self.add_log)
        log_button.pack(pady=5)

        back_page = tk.Button(self, text="Go to Page 1", command=lambda: controller.show_frame("Page1"))
        back_page.pack(pady=5)

        global_log_page = tk.Button(self, text="View Global Log", command=lambda: controller.show_frame("GlobalLogPage"))
        global_log_page.pack(pady=5)

    def add_log(self):
        """Thêm log từ trang 2"""
        self.controller.logger.add_log("Log added from Page 2")


# Trang hiển thị log toàn cục
class GlobalLogPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Global Log Viewer", font=("Arial", 16))
        label.pack(pady=10)

        # Hiển thị log toàn cục
        self.log_viewer = LogDisplay(self, logger=controller.logger)
        self.log_viewer.pack(fill="both", expand=True)

        refresh_button = tk.Button(self, text="Refresh Logs", command=self.log_viewer.update_logs)
        refresh_button.pack(pady=5)

        back_button = tk.Button(self, text="Back to Page 1", command=lambda: controller.show_frame("Page1"))
        back_button.pack(pady=5)


# Chạy ứng dụng
if __name__ == "__main__":
    app = App()
    app.mainloop()
