import tkinter as tk
from Interface.TextInterface.TextInterface import TextInterface
from Interface.ImageInterface.ImageInterface import ImageInterface
from Interface.AudioInterface.AudioInterface import AudioInterface
from Interface.VideoInterface.VideoInterface import VideoInterface
from Interface.DecryptionInterface.DecryptionInterface import DecryptionInterface
from PIL import Image, ImageTk  # Import thư viện Pillow

class NavbarMini(tk.Frame):
    def __init__(self, master, state, update_state_func):
        super().__init__(master, bg="#f0f8ff", bd=2, relief="groove")
        self.master = master
        self.state = state
        self.update_state = update_state_func
        self.icons = {}

        self.add_logo()
        self.load_icons()

        self.buttons = []
        self.create_button("text", TextInterface, 1)
        self.create_button("image", ImageInterface, 2)
        self.create_button("audio", AudioInterface, 3)
        self.create_button("video", VideoInterface, 4)
        self.create_button("decrypt_ai", DecryptionInterface, 5)

    def add_logo(self):
        try:
            logo_img = Image.open("Images/logo.png")
            logo_img = logo_img.resize((50, 50), Image.ANTIALIAS)
            logo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(self, image=logo, bg="#f0f8ff")
            logo_label.image = logo
            logo_label.grid(row=0, column=0, pady=5, padx=5, sticky="n")
        except Exception as e:
            print(f"Could not load logo: {e}")

    def load_icons(self):
        icons_data = {
            "text": "Images/text_icon.png",
            "image": "Images/image_icon.png",
            "audio": "Images/audio_icon.png",
            "video": "Images/video_icon.png",
            "decrypt_ai": "Images/AI_icon.png",
        }
        for name, path in icons_data.items():
            try:
                img = Image.open(path)
                img = img.resize((40, 40), Image.ANTIALIAS)
                self.icons[name] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Could not load icon {name}: {e}")

    def create_button(self, icon_name, interface, row_idx):
        if icon_name not in self.icons:
            print(f"Icon {icon_name} not found")
            return
        canvas = tk.Canvas(self, width=50, height=50, bg="#f0f8ff", bd=0, highlightthickness=0, relief="flat")
        canvas.grid(row=row_idx, column=0, padx=10, pady=10, sticky="ew")

        canvas.create_oval(5, 5, 45, 45, fill="#cceeff", outline="#f0f8ff", width=0)
        canvas.create_image(25, 25, image=self.icons[icon_name])

        canvas.bind("<Button-1>", lambda event: self.on_click(event, canvas, interface))
        self.buttons.append((canvas, interface))

    def on_click(self, event, canvas, interface):
        # Đổi màu nút khi click để nhận diện trang hiện tại
        def apply_click_color():
            canvas.config(bg="#cceeff")  # Màu khi click (màu đậm)
            self.update_state(interface)  # Cập nhật trạng thái sau khi thay đổi màu

        # Áp dụng màu click sau một khoảng thời gian ngắn
        canvas.after(50, apply_click_color)

    def highlight_selected_button(self, selected_interface):
        for canvas, iface in self.buttons:
            if iface == selected_interface:
                canvas.config(bg="#cceeff")  # Nút được chọn với màu xanh nổi bật (màu đậm)
            else:
                canvas.config(bg="#f0f8ff")  # Màu nền ban đầu của nút
