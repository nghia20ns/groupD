import tkinter as tk
from Interface.DecryptionInterface.TextInterface import TextInterface
from Interface.DecryptionInterface.ImageInterface import ImageInterface
from Interface.DecryptionInterface.AudioInterface import AudioInterface
from Interface.DecryptionInterface.VideoInterface import VideoInterface

class DecryptionInterface(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")


        # Header
        self.header_frame = tk.Frame(self, bg="#f0f8ff", relief="ridge", bd=2)
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=5)

        # Nút text
        self.text_btn = tk.Button(self.header_frame, text="Text decrypt", command=self.switch_to_text,
                                     bg="#e6f7ff", fg="black", font=("Helvetica", 10), relief="flat",
                                     width=12, height=1, cursor="hand2",)
        self.text_btn.grid(row=0, column=0, padx=15, pady=10)


        # Nút Image
        self.image_btn = tk.Button(self.header_frame, text="Image decrypt", command=self.switch_to_image ,
                                     bg="#e6f7ff", fg="black", font=("Helvetica", 10), relief="flat",
                                     width=12, height=1, cursor="hand2",)
        self.image_btn.grid(row=0, column=1, padx=15, pady=10)
        # Nút text
        self.audio_btn = tk.Button(self.header_frame, text="Audio decrypt", command=self.switch_to_audio,
                                     bg="#e6f7ff", fg="black", font=("Helvetica", 10), relief="flat",
                                     width=12, height=1, cursor="hand2",)
        self.audio_btn.grid(row=0, column=2, padx=15, pady=10)
        # Nút text
        self.video_btn = tk.Button(self.header_frame, text="Video decrypt", command=self.switch_to_video,
                                     bg="#e6f7ff", fg="black", font=("Helvetica", 10), relief="flat",
                                     width=12, height=1, cursor="hand2",)
        self.video_btn.grid(row=0, column=3, padx=15, pady=10)

        # Cấu hình grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Component cho Text
        self.text_component = TextInterface(self)
        self.text_component.grid(row=1, column=0, pady=20, sticky="nsew")  # Dùng grid thay vì pack

        # Component cho Image
        self.image_component = ImageInterface(self)
        self.image_component.grid(row=1, column=0, pady=20, sticky="nsew")

        # Component cho Audio
        self.audio_component = AudioInterface(self)
        self.audio_component.grid(row=1, column=0, pady=20, sticky="nsew")  # Dùng grid thay vì pack

        # Component cho Video
        self.video_component = VideoInterface(self)
        self.video_component.grid(row=1, column=0, pady=20, sticky="nsew")
                # Bottom section
        self.bottom_frame = tk.Frame(self, bg="#e6f7ff")
        self.bottom_frame.grid(row=2, column=0, sticky="ew", pady=10)

        # Hiệu ứng hover cho nút
        self.add_hover_effect(self.text_btn)
        self.add_hover_effect(self.image_btn)
        self.add_hover_effect(self.audio_btn)
        self.add_hover_effect(self.video_btn)

        # Biến trạng thái mặt định
        self.current_state = "Text Encrypt"  # Mặc định là Encode
        self.text_btn.config(state=tk.DISABLED, bg="#cceeff", fg="white")
        self.image_btn.config(state=tk.NORMAL, bg="#e6f7ff", fg="black")
        self.audio_btn.config(state=tk.NORMAL, bg="#e6f7ff", fg="black")
        self.video_btn.config(state=tk.NORMAL, bg="#e6f7ff", fg="black")

        self.image_component.grid_forget()
        self.audio_component.grid_forget()
        self.video_component.grid_forget()

        self.text_component.grid(row=1, column=0, pady=20, sticky="nsew")
        # Footer 
        self.footer_label = tk.Label(self, text="© Võ Quốc Nghĩa | quocnghia91ll@gmail.com", 
                                    font=("Helvetica", 10), fg="#888", bg="white")
        self.footer_label.grid(row=2, column=0, pady=10, sticky="s")  # Placing at the bottom row with sticky="s"

    def switch_to_text(self):
        if self.current_state != "Text Encrypt":
            self.current_state = "Text Encrypt"
            self.text_btn.config(state=tk.DISABLED, bg="#cceeff", fg="white")
            self.text_component.grid(row=1, column=0, pady=20, sticky="nsew")
            self.image_btn.config(state=tk.NORMAL, bg="#e6f7ff", fg="black")
            self.image_component.grid_forget()
            self.audio_btn.config(state=tk.NORMAL, bg="#e6f7ff", fg="black")
            self.audio_component.grid_forget()
            self.video_btn.config(state=tk.NORMAL, bg="#e6f7ff", fg="black")
            self.video_component.grid_forget()
    def switch_to_image(self):
        if self.current_state != "Image Encrypt":
            self.current_state = "Image Encrypt"
            self.image_btn.config(state=tk.DISABLED, bg="#cceeff", fg="white")
            self.image_component.grid(row=1, column=0, pady=20, sticky="nsew")
            self.text_btn.config(state=tk.NORMAL, bg="#e6f7ff", fg="black")
            self.text_component.grid_forget()
            self.audio_btn.config(state=tk.NORMAL, bg="#e6f7ff", fg="black")
            self.audio_component.grid_forget()
            self.video_btn.config(state=tk.NORMAL, bg="#e6f7ff", fg="black")
            self.video_component.grid_forget()
    def switch_to_audio(self):
        if self.current_state != "Audio Encrypt":
            self.current_state = "Audio Encrypt"
            self.audio_btn.config(state=tk.DISABLED, bg="#cceeff", fg="white")
            self.audio_component.grid(row=1, column=0, pady=20, sticky="nsew")

            self.image_btn.config(state=tk.NORMAL, bg="#e6f7ff", fg="black")
            self.image_component.grid_forget()
            self.text_btn.config(state=tk.NORMAL, bg="#e6f7ff", fg="black")
            self.text_component.grid_forget()
            self.video_btn.config(state=tk.NORMAL, bg="#e6f7ff", fg="black")
            self.video_component.grid_forget()
    def switch_to_video(self):
        if self.current_state != "Video Encrypt":
            self.current_state = "Video Encrypt"
            self.video_btn.config(state=tk.DISABLED, bg="#cceeff", fg="white")
            self.video_component.grid(row=1, column=0, pady=20, sticky="nsew")

            self.image_btn.config(state=tk.NORMAL, bg="#e6f7ff", fg="black")
            self.image_component.grid_forget()
            self.audio_btn.config(state=tk.NORMAL, bg="#e6f7ff", fg="black")
            self.audio_component.grid_forget()
            self.text_btn.config(state=tk.NORMAL, bg="#e6f7ff", fg="black")
            self.text_component.grid_forget()
    def add_hover_effect(self, button):
        """Thêm hiệu ứng hover cho nút."""
        def on_enter(event):
            if button['state'] != tk.DISABLED:
                button.config(bg="#cceeff", fg="white")  # Màu khi hover
        def on_leave(event):
            if button['state'] != tk.DISABLED:
                button.config(bg="#e6f7ff", fg="black")  # Màu mặc định
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)


# Code chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Decryption With AI")
    root.geometry("800x600")
    root.resizable(False, False)

    app = DecryptionInterface(root, None)
    app.pack(fill="both", expand=True)

    root.mainloop()
