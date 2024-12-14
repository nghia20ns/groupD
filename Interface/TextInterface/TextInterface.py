import tkinter as tk
from Interface.TextInterface.EncodeComponent import EncodeComponent
from Interface.TextInterface.DecodeComponent import DecodeComponent

class TextInterface(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")


        # Header
        self.header_frame = tk.Frame(self, bg="#f0f8ff", relief="ridge", bd=2)
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=5)

        # Nút Encode
        self.encode_btn = tk.Button(self.header_frame, text="Encrypt", command=self.switch_to_encode,
                                     bg="#e6f7ff", fg="black", font=("Helvetica", 10), relief="flat",
                                     width=12, height=1, cursor="hand2",)
        self.encode_btn.grid(row=0, column=0, padx=15, pady=10)

        # Nút Decode
        self.decode_btn = tk.Button(self.header_frame, text="Decrypt", command=self.switch_to_decode,
                                     bg="#e6f7ff", fg="black", font=("Helvetica", 10), relief="flat",
                                     width=12, height=1, cursor="hand2")
        self.decode_btn.grid(row=0, column=1, padx=15, pady=10)

        # Cấu hình grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Component Encode và Decode
        self.encode_component = EncodeComponent(self)
        self.encode_component.grid(row=1, column=0, pady=20, sticky="nsew")

        self.decode_component = DecodeComponent(self)
        self.decode_component.grid(row=1, column=0, pady=20, sticky="nsew")
        self.decode_component.grid_forget()  # Ẩn Decode mặc định

        # Hiệu ứng hover cho nút
        self.add_hover_effect(self.encode_btn)
        self.add_hover_effect(self.decode_btn)

        # Biến trạng thái mặt định
        self.current_state = "Encrypt"  # Mặc định là Encode
        self.encode_btn.config(state=tk.DISABLED, bg="#cceeff", fg="white")
        self.decode_btn.config(state=tk.NORMAL, bg="#e6f7ff", fg="black")
        self.decode_component.grid_forget()
        self.encode_component.grid(row=1, column=0, pady=20, sticky="nsew")

        # Footer 
        self.footer_label = tk.Label(self, text="© Võ Quốc Nghĩa | quocnghia91ll@gmail.com", 
                                    font=("Helvetica", 10), fg="#888", bg="white")
        self.footer_label.grid(row=2, column=0, pady=10, sticky="s")  # Placing at the bottom row with sticky="s"

    def switch_to_encode(self):
        if self.current_state != "Encrypt":
            self.current_state = "Encrypt"
            self.encode_btn.config(state=tk.DISABLED, bg="#cceeff", fg="black")
            self.decode_btn.config(state=tk.NORMAL, bg="#e6f7ff", fg="black")
            self.decode_component.grid_forget()
            self.encode_component.grid(row=1, column=0, pady=20, sticky="nsew")

    def switch_to_decode(self):
        if self.current_state != "Decrypt":
            self.current_state = "Decrypt"
            self.encode_btn.config(state=tk.NORMAL, bg="#e6f7ff", fg="black")
            self.decode_btn.config(state=tk.DISABLED, bg="#cceeff", fg="black")
            self.encode_component.grid_forget()
            self.decode_component.grid(row=1, column=0, pady=20, sticky="nsew")

    # hiệu ứng di chuột
    def add_hover_effect(self, widget):
        def on_enter(event):
            if widget['bg'] not in ("#66b3ff", "#cceeff"):
                widget['bg'] = "#99ddff"
        def on_leave(event):
            if widget['bg'] not in ("#66b3ff", "#cceeff"):
                widget['bg'] = "#e6f7ff"
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)



# Code chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Video Steganography")
    root.geometry("800x600")
    root.resizable(False, False)

    app = TextInterface(root, None)
    app.pack(fill="both", expand=True)

    root.mainloop()
