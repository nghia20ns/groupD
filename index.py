import tkinter as tk

class IndexApp(tk.Frame):
    def __init__(self, master, extra_param=None):
        super().__init__(master, bg="#cceeff", bd=2, relief="groove")
        self.master = master
        self.extra_param = extra_param  # Use extra parameter if needed
        self.pack(fill="both", expand=True)

        # Create a canvas for gradient background
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.grid(row=0, column=0, rowspan=5, sticky="nsew")

        # Create gradient background on canvas
        self.canvas.create_rectangle(0, 0, 900, 650, fill="#cceeff", outline="#cceeff")
        self.canvas.create_rectangle(0, 0, 900, 650, fill="lightblue", outline="lightblue")

        # Title of the page
        self.title_label = tk.Label(self, text="Chào mừng đến với Steganography Tool", font=("Helvetica", 24, "bold"), fg="#4CAF50", bg="#cceeff")
        self.title_label.grid(row=1, column=0, pady=20)

        # Descriptive text
        self.description_label = tk.Label(self, text="Ứng dụng Steganography này giúp bạn ẩn thông tin vào hình ảnh.\n"
                                                     "Hãy thử nhấn nút bên dưới để bắt đầu!", font=("Helvetica", 14), fg="#333", bg="#cceeff")
        self.description_label.grid(row=2, column=0, pady=10)

        # Start button
        self.start_button = tk.Button(self, text="Bắt đầu", font=("Helvetica", 14), fg="#fff", bg="#4CAF50", command=self.start_process)
        self.start_button.grid(row=3, column=0, pady=20)

        # Create a footer label
        self.footer_label = tk.Label(self, text="© 2024 Công ty ABC | Tất cả quyền được bảo lưu.", font=("Helvetica", 10), fg="#888", bg="#cceeff")
        self.footer_label.grid(row=5, column=0, pady=10, sticky="s")

        # Create a frame for detailed information
        self.frame = tk.Frame(self, bg="#ffffff", relief="solid", bd=2)
        self.frame.grid(row=4, column=0, pady=20, padx=30, sticky="nsew")

        # Title for the frame
        self.frame_title = tk.Label(self.frame, text="Thông tin chi tiết về Steganography", font=("Helvetica", 16, "bold"), bg="#ffffff")
        self.frame_title.grid(row=0, column=0, pady=10)

        # Description inside the frame
        self.frame_description = tk.Label(self.frame, text="Ứng dụng này sử dụng thuật toán Steganography để giấu thông tin trong ảnh.\n"
                                                            "Bạn có thể tải lên ảnh và nhập văn bản để ẩn giấu thông tin vào ảnh.\n"
                                                            "Sau đó, bạn có thể giải mã thông tin đã giấu.", font=("Helvetica", 12), fg="#333", bg="#ffffff")
        self.frame_description.grid(row=1, column=0, pady=10)

    def start_process(self):
        # Function triggered when the "Bắt đầu" button is clicked
        self.description_label.config(text="Hãy chọn ảnh và nhập thông tin để bắt đầu ẩn thông tin.")
        self.start_button.config(state="disabled")  # Disable the button after starting process


if __name__ == "__main__":
    root = tk.Tk()
    app = IndexApp(root)
    root.title("Steganography Tool")
    root.geometry("900x650")  # Window size
    root.grid_rowconfigure(0, weight=1)  # Ensures the canvas takes up available space
    root.grid_columnconfigure(0, weight=1)  # Ensures the main content area is responsive
    app.mainloop()
