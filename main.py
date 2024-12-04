import tkinter as tk
from NavBar import Navbar
from tkinter import PhotoImage
from NavabarMini import NavbarMini
from index import IndexApp

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        # Khởi tạo Navbar và NavbarMini
        self.navbar = Navbar(self, self.state, self.update_state)
        self.navbarMini = NavbarMini(self, self.state, self.update_state)

        # Navbar được gắn vào phía trái
        self.navbar.pack(side="left", fill="y")

        # Tạo ảnh cho nút toggle và thay đổi kích thước
        self.original_image = PhotoImage(file="Images/img_nv.png")
        self.resized_image = self.original_image.subsample(120, 120)  # Giảm kích thước ảnh

        # Nút toggle navbar
        self.toggle_button = tk.Button(self, image=self.resized_image, command=self.toggle_navbar, bg="#99c2ff", borderwidth=0, relief="raised")
        self.toggle_button.place(x=770, y=60)  # Vị trí của nút toggle

        # Frame chứa nội dung
        self.content_frame = tk.Frame(self)  
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Biến trạng thái
        self.state = None
        self.current_interface = None
        
        # Nút floating button
        self.floating_button = tk.Button(self, image=self.resized_image, command=self.floating_button_action, bg="#99c2ff", borderwidth=0, relief="raised")
        self.floating_button.place(x=180, y=60)  # Vị trí của floating button
        self.show_interface(IndexApp)
        # Khởi tạo trạng thái mặc định là Navbar
        self.current_state = "Navbar"  
        self.navbarMini.pack_forget()  # Ẩn navbarMini ban đầu

    def floating_button_action(self):
        """Đổi trạng thái hiển thị của navbar và thay đổi vị trí nút floating."""
        if self.navbar.winfo_ismapped():
            self.navbarMini.pack(side="left", fill="y")  # Hiển thị navbar mini
            self.navbar.pack_forget()  # Ẩn navbar chính
            self.floating_button.place(x=70, y=60)  # Di chuyển nút floating
        else:
            self.navbar.pack(side="left", fill="y")  # Hiển thị navbar chính
            self.navbarMini.pack_forget()  # Ẩn navbar mini
            self.floating_button.place(x=180, y=60)  # Di chuyển nút floating về vị trí ban đầu

    def show_interface(self, interface_class):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        """Hiển thị giao diện đã chọn."""
        if self.current_interface is not None:
            self.current_interface.destroy()

        self.current_interface = interface_class(self.content_frame)
        self.current_interface.pack(fill="both", expand=True)

    def update_state(self, interface_class):
        """Cập nhật trạng thái và làm nổi bật nút đã chọn."""
        self.state = interface_class
        self.navbar.highlight_selected_button(interface_class)
        self.navbarMini.highlight_selected_button(interface_class)
        self.show_interface(interface_class)

    def toggle_navbar(self):
        """Toggle việc hiển thị navbar chính."""
        if self.navbar.winfo_ismapped():
            self.navbar.pack_forget()  # Ẩn navbar
        else:
            self.navbar.pack(side="left", fill="y")  # Hiển thị navbar

if __name__ == "__main__":
    app = MainApplication()
    app.title("Steganography Tool")
    app.geometry("1000x650")  # Kích thước cửa sổ ban đầu

    # Thiết lập kích thước tối thiểu của cửa sổ
    app.minsize(1000, 650)  # Kích thước tối thiểu là 900x650

    app.mainloop()
