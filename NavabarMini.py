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
                img = img.resize((25, 25), Image.ANTIALIAS)
                self.icons[name] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Could not load icon {name}: {e}")

    def create_button(self, icon_name, interface, row_idx):
        if icon_name not in self.icons:
            print(f"Icon {icon_name} not found")
            return
        
        canvas = tk.Canvas(self, width=50, height=50, bd=0,
                            bg="#f0f8ff", highlightthickness=0, relief="flat")
        canvas.grid(row=row_idx, column=0, padx=10, pady=10, sticky="ew")

        # Tạo một hình oval và lưu ID của nó để sau này thay đổi
        oval_id = canvas.create_oval(5, 5, 45, 45, outline="#f0f8ff", fill="#f0f8ff", width=0)
        canvas.create_image(25, 25, image=self.icons[icon_name])

        # Thêm sự kiện khi click vào nút
        canvas.bind("<Button-1>", lambda event: self.on_click(event, canvas, interface, oval_id))
        self.buttons.append((canvas, interface, oval_id))
        self.add_hover_effect(canvas, oval_id)

    def on_click(self, event, canvas, interface, oval_id):
        # Thay đổi màu nút khi click
        def apply_click_color():
            self.update_state(interface)  # Cập nhật trạng thái sau khi thay đổi màu

        canvas.after(50, apply_click_color)

    def add_hover_effect(self, canvas, oval_id):
        # Tạo một hình lớn hơn bao quanh hình oval hiện tại để mở rộng phạm vi di chuột vào
        bounding_oval_id = canvas.create_oval(
            canvas.bbox(oval_id)[0] - 10,  # Dịch sang trái
            canvas.bbox(oval_id)[1] - 10,  # Dịch lên trên
            canvas.bbox(oval_id)[2] + 10,  # Dịch sang phải
            canvas.bbox(oval_id)[3] + 10,  # Dịch xuống dưới
            outline='', fill='', tags='hover_area'  # Không có viền, không màu sắc
        )
        def on_enter(event):
            # Lấy màu hiện tại của hình oval
            current_fill = canvas.itemcget(oval_id, 'fill')
            if current_fill not in ("#66b3ff", "#99ddff"):
                canvas.itemconfig(oval_id, fill="#cceeff")  # 99ddff Thay đổi màu của hình oval khi di chuột vào
        def on_leave(event):
            # Lấy màu hiện tại của hình oval
            current_fill = canvas.itemcget(oval_id, 'fill')
            if current_fill not in ("#66b3ff", "#99ddff"):
                canvas.itemconfig(oval_id, fill="#e6f7ff")  # Đặt lại màu của hình oval khi di chuột rời khỏi

        # Ràng buộc sự kiện di chuột vào và rời khỏi cho vùng bao quanh lớn hơn
        canvas.tag_bind(bounding_oval_id, "<Enter>", on_enter)
        canvas.tag_bind(bounding_oval_id, "<Leave>", on_leave)
        # Xóa vùng bao quanh lớn hơn sau khi hoàn thành
        canvas.tag_bind(oval_id, "<Leave>", lambda event: canvas.delete(bounding_oval_id))

    def highlight_selected_button(self, selected_interface):
        for canvas, iface, oval_id in self.buttons:
            if iface == selected_interface:
                canvas.itemconfig(oval_id, fill="#99ddff",state=tk.DISABLED)  # Thay đổi màu của hình oval khi chọn
            else:
                canvas.itemconfig(oval_id, fill="#f0f8ff",state=tk.NORMAL)  # Đặt lại màu ban đầu của hình oval
