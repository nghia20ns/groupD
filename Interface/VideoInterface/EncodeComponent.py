import tkinter as tk
from tkinter import filedialog
from binary import *
from matplotlib import pyplot as plt
import cv2
import json
import numpy as np
import os
from tkinter import ttk
import tkinter
from PIL import Image, ImageTk
from Logger import LogDisplay, Logger

class EncodeComponent(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")

        self.grid(sticky="nsew")
        
        
        # Set up grid weight configuration
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_rowconfigure(8, weight=0)
        self.grid_rowconfigure(9, weight=0)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        # Title Label with bold font for emphasis
        label = tk.Label(self, text="Video Encryption", font=("Arial", 18, "bold"), bg="white")
        label.grid(row=0, column=0, columnspan=3, padx=20, pady=20)


        # Text Entry
        lbl_text = tk.Label(self, text="Text to encrypt:", bg="white", font=("Arial", 12))
        lbl_text.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.edit_entry_text = ttk.Entry(self, width=30, font=("Arial", 12))
        self.edit_entry_text.grid(row=1, column=1, pady=10, sticky="we")

        # Label và Entry cho frame cần giải mã
        lbl_frame = tk.Label(self, text="Number frame:", bg="white", font=("Arial", 12))
        lbl_frame.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.edit_entry_frame = ttk.Entry(self, width=30, font=("Arial", 12))
        self.edit_entry_frame.grid(row=2, column=1, pady=10, sticky="we")
        self.edit_entry_frame.grid_columnconfigure(1, weight=1)  # Đảm bảo ô nhập văn bản mở rộng theo chiều ngang


        # Password Entry
        lbl_pass = tk.Label(self, text="Password:", bg="white", font=("Arial", 12))
        lbl_pass.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.edit_entry_pass = ttk.Entry(self, width=30, font=("Arial", 12), show="*")
        self.edit_entry_pass.grid(row=3, column=1, pady=10, sticky="we")
        # Load eye icon images (open and closed)
        self.eye_open = Image.open("eye_open.png")  # Image for eye open
        self.eye_open = self.eye_open.resize((20, 20), Image.ANTIALIAS)
        self.eye_open_icon = ImageTk.PhotoImage(self.eye_open)
        self.eye_closed = Image.open("eye_close.png")  # Image for eye closed
        self.eye_closed = self.eye_closed.resize((20, 20), Image.ANTIALIAS)
        self.eye_closed_icon = ImageTk.PhotoImage(self.eye_closed)
        # Button to toggle password visibility
        self.toggle_eye_button = tk.Button(self, image=self.eye_closed_icon, bg="white", bd=0, command=self.toggle_password)
        self.toggle_eye_button.grid(row=3, column=2, padx=10)
        # Radio Button encryption algorithm
        lbl_text = tk.Label(self, text="Encryption algorithm:", bg="white", font=("Arial", 12))
        lbl_text.grid(row=4, column=0, padx=10, pady=10, sticky="e")

        # Frame for RadioButton options
        self.buttons_frame = tk.Frame(self, bg="white")
        self.buttons_frame.grid(row=4, column=1, pady=10)
        # RadioButton options
        status_options = ["XOR Cipher", "Vigenère Cipher", "RC4"]
        self.algorithm = tk.IntVar()
        for index in range(len(status_options)):
            radio_button = tk.Radiobutton(
                self.buttons_frame,
                text=status_options[index],
                variable=self.algorithm,
                value=index,
                padx=5,
                font=("Arial", 10),  # Adjust font size
                bg="white"        # Adjust background color
            )
            radio_button.grid(row=0, column=index, padx=5)



        # File Path Entry
        lbl_file = tk.Label(self, text="File Encode:", bg="white", font=("Arial", 12))
        lbl_file.grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.file_path_entry = ttk.Entry(self, width=50, font=("Arial", 12))
        self.file_path_entry.grid(row=5, column=1, pady=10, sticky="we")
        browse_button = ttk.Button(self, text="...", command=self.browse_file, width=5)
        browse_button.grid(row=5, column=2, padx=10, pady=10)

        # Folder Path Save Entry
        lbl_browser_folder = tk.Label(self, text="Folder Path Save:", bg="white", font=("Arial", 12))
        lbl_browser_folder.grid(row=6, column=0, padx=10, pady=10, sticky="e")
        self.folder_path_entry_save = ttk.Entry(self, width=50, font=("Arial", 12))
        self.folder_path_entry_save.grid(row=6, column=1, pady=10, sticky="we")
        browse_button_save = ttk.Button(self, text="...", command=self.browse_folder, width=5)
        browse_button_save.grid(row=6, column=2, padx=10, pady=10)

        # New File Name Entry
        lbl_image = tk.Label(self, text="Name New File:", bg="white", font=("Arial", 12))
        lbl_image.grid(row=7, column=0, padx=10, pady=10, sticky="e")
        self.new_video = ttk.Entry(self, width=30, font=("Arial", 12))
        self.new_video.grid(row=7, column=1, pady=10, sticky="we")

        # Submit Button
        submit_button = ttk.Button(self, text="Encode", command=self.submit, width=30)
        submit_button.grid(row=8, column=1, padx=10, pady=20, sticky="e")

        #Log
        self.logger = Logger("app_log.txt")
        self.log_display = LogDisplay(self, self.logger)
        self.log_display.grid(row=9, column=0, columnspan=3, sticky="nsew")



    def toggle_password(self):
        # Toggle the password visibility
        if self.edit_entry_pass.cget("show") == "*":
            self.edit_entry_pass.config(show="")  # Show the password
            self.toggle_eye_button.config(image=self.eye_open_icon)  # Switch to open eye icon
        else:
            self.edit_entry_pass.config(show="*")  # Hide the password
            self.toggle_eye_button.config(image=self.eye_closed_icon)  # Switch to closed eye icon

    def browse_file(self):
        filename = filedialog.askopenfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
        )
        
        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(0, filename)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        self.folder_path_entry_save.delete(0, tk.END)  # Xóa nội dung trong entry trước khi cập nhật
        self.folder_path_entry_save.insert(0, folder_path)  # Thêm đường dẫn thư mục đã chọn vào entry

    def submit(self):

        self.encode_vid_data()
        
    def embed(self,frame,message,password):
        
        algorithm = self.algorithm.get()
        if (algorithm == 0):
            message = binary.xor_cipher(message,password)
        elif (algorithm == 1):
            message = binary.vigenere_encrypt(message,password)
        else:      
            message = binary.rc4_encrypt(message,password)

        print("The encrypted data is : ",message)
        if (len(message) == 0): 
            raise ValueError('Data entered to be encoded is empty')
        if not message:
            self.log_display.add_log("Lỗi", "Dữ liệu nhập để mã hóa không được để trống!")
            return

        message +='*^*^*'
        
        binary_data=binary.msgtobinary(message)
        length_data = len(binary_data)
        
        index_data = 0
        
        for i in frame:
            for pixel in i:
                r, g, b = binary.msgtobinary(pixel)
                if index_data < length_data:
                    pixel[0] = int(r[:-1] + binary_data[index_data], 2) 
                    index_data += 1
                if index_data < length_data:
                    pixel[1] = int(g[:-1] + binary_data[index_data], 2) 
                    index_data += 1
                if index_data < length_data:
                    pixel[2] = int(b[:-1] + binary_data[index_data], 2) 
                    index_data += 1
                if index_data >= length_data:
                    break
            return frame# Kiểm tra
    def encode_vid_data(self):
        # Lấy thư mục và tên file
        folder_path = self.folder_path_entry_save.get()
        file_video_name = self.new_video.get()
        # Kiểm tra xem người dùng có chọn thư mục lưu không
        if not folder_path:
            self.log_display.add_log("Please select a folder to save the file.")
            return
        
        # Kiểm tra tên file và thêm đuôi .mp4 nếu chưa có
        if not file_video_name.endswith(".mp4"):
            file_video_name += ".mp4"

        file_frame_name = file_video_name
        if file_frame_name.endswith(".mp4"):
            file_frame_name = file_frame_name[:-4] + ".txt"

        # Kết hợp đường dẫn đầy đủ
        full_video_path = os.path.join(folder_path, file_video_name)
        full_frame_path = os.path.join(folder_path, file_frame_name)

        # Mở video nguồn
        source_video_path = self.file_path_entry.get()
        if not os.path.exists(source_video_path):
            self.log_display.add_log("Source video file not found.")
            return

        cap = cv2.VideoCapture(source_video_path)
        if not cap.isOpened():
            self.log_display.add_log("Unable to open the source video file.")
            return
        
        # Thiết lập các thông số cho video đầu ra
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        size = (frame_width, frame_height)
        out = cv2.VideoWriter(full_video_path, fourcc, 25.0, size)

        # Đếm tổng số frame trong video
        max_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print("Total number of frames in selected video:", max_frame)

        # Kiểm tra và xử lý số frame để mã hóa
        try:
            n = int(self.edit_entry_frame.get())
            if n > max_frame or n <= 0:
                self.log_display.add_log(f"Frame number must be between 1 and {max_frame}.")
                return
        except ValueError:
            self.log_display.add_log("Please enter a valid integer for the frame number.")
            return

        # Lấy dữ liệu mã hóa và mật khẩu
        message = self.edit_entry_text.get() 
        password = self.edit_entry_pass.get()
        if not message or not password:
            self.log_display.add_log("Message and password cannot be empty.")
            return

        frame_number = 0
        frame_to_save = None  # Biến để lưu frame đã mã hóa

        while cap.isOpened():
            frame_number += 1
            ret, frame = cap.read()
            if not ret:
                break

            # Thực hiện mã hóa trên frame chỉ định
            if frame_number == n:
                frame_with_data = self.embed(frame, message, password)
                frame_to_save = frame_with_data
                frame = frame_with_data

            out.write(frame)
        
        # Giải phóng các tài nguyên
        cap.release()
        out.release()

        # Lưu frame đã mã hóa vào file JSON nếu có
        if frame_to_save is not None:
            with open(full_frame_path, "w") as f:
                json.dump(frame_to_save.tolist(), f)
            self.log_display.add_log("\nData encoded into video and saved frame to "+ file_frame_name)
        else:
            self.log_display.add_log("Error: Specified frame not found for embedding.")

        return


if __name__ == "__main__":
    root = tk.Tk()
    decode_component = EncodeComponent(root)
    decode_component.pack(fill="both", expand=True)
    root.mainloop()
