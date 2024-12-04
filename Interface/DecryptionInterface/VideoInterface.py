import tkinter as tk
from tkinter import filedialog
from binary import *
import os
import cv2
import json
from tkinter import ttk
import tkinter
from PIL import Image, ImageTk
from CiperType import CiperType
from Logger import LogDisplay, Logger

class VideoInterface(tk.Frame):
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

        # Tiêu đề
        label = tk.Label(self, text="Video Decryption", font=("Arial", 18, "bold"), bg="white")
        label.grid(row=0, column=0, columnspan=3, padx=20, pady=20)
        
        # Button "Browse video File" và Entry "File Path"
        lbl_browser_video = tk.Label(self, text="File Decrypt:", bg="white", font=("Arial", 12))
        lbl_browser_video.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.file_path_video = ttk.Entry(self, width=50, font=("Arial", 12))
        self.file_path_video.grid(row=1, column=1, pady=10, sticky="we")
        browse_button_video = ttk.Button(self, text="...", command=self.browse_file_video, width=5)
        browse_button_video.grid(row=1, column=2, padx=10, pady=10)

        # Button "Browse video File" và Entry "File Path"
        lbl_browser_frame = tk.Label(self, text="Frame Decrypt:", bg="white", font=("Arial", 12))
        lbl_browser_frame.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.file_path_frame = ttk.Entry(self, width=50, font=("Arial", 12))
        self.file_path_frame.grid(row=2, column=1, pady=10, sticky="we")
        browse_button_frame = ttk.Button(self, text="...", command=self.browse_file_frame, width=5)
        browse_button_frame.grid(row=2, column=2, padx=10, pady=10)

        # Label và Entry cho frame cần giải mã
        lbl_frame = tk.Label(self, text="Number frame:", bg="white", font=("Arial", 12))
        lbl_frame.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.edit_entry_frame = ttk.Entry(self, width=30, font=("Arial", 12))
        self.edit_entry_frame.grid(row=3, column=1, pady=10, sticky="we")
        self.edit_entry_frame.grid_columnconfigure(1, weight=1)  # Đảm bảo ô nhập văn bản mở rộng theo chiều ngang


        # Password Entry
        lbl_pass = tk.Label(self, text="Password:", bg="white", font=("Arial", 12))
        lbl_pass.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.edit_entry_pass = ttk.Entry(self, width=30, font=("Arial", 12), show="*")
        self.edit_entry_pass.grid(row=4, column=1, pady=10, sticky="we")

        # Load eye icon images (open and closed)
        self.eye_open = Image.open("eye_open.png")  # Image for eye open
        self.eye_open = self.eye_open.resize((20, 20), Image.ANTIALIAS)
        self.eye_open_icon = ImageTk.PhotoImage(self.eye_open)
        self.eye_closed = Image.open("eye_close.png")  # Image for eye closed
        self.eye_closed = self.eye_closed.resize((20, 20), Image.ANTIALIAS)
        self.eye_closed_icon = ImageTk.PhotoImage(self.eye_closed)
        # Button to toggle password visibility
        self.toggle_eye_button = tk.Button(self, image=self.eye_closed_icon, bg="white", bd=0, command=self.toggle_password)
        self.toggle_eye_button.grid(row=4, column=2, padx=10)

        # Folder Path Save Entry
        lbl_browser_folder = tk.Label(self, text="Folder Path Save:", bg="white", font=("Arial", 12))
        lbl_browser_folder.grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.folder_path_entry_save = ttk.Entry(self, width=50, font=("Arial", 12))
        self.folder_path_entry_save.grid(row=5, column=1, pady=10, sticky="we")
        browse_button_save = ttk.Button(self, text="...", command=self.browse_folder, width=5)
        browse_button_save.grid(row=5, column=2, padx=10, pady=10)

        # New File Name Entry
        lbl_txt = tk.Label(self, text="Name New File:", bg="white", font=("Arial", 12))
        lbl_txt.grid(row=6, column=0, padx=10, pady=10, sticky="e")
        self.new_txt = ttk.Entry(self, width=30, font=("Arial", 12))
        self.new_txt.grid(row=6, column=1, pady=10, sticky="we")

        # Submit Button with hover effect
        submit_button = ttk.Button(self, text="Encode", command=self.submit, width=30)
        submit_button.grid(row=7, column=1, padx=10, pady=20, sticky="e")

        #Log
        self.logger = Logger("app_log.txt")
        self.log_display = LogDisplay(self, self.logger)
        self.log_display.grid(row=8, column=0, columnspan=3, sticky="nsew")

    def toggle_password(self):
        # Toggle the password visibility
        if self.edit_entry_pass.cget("show") == "*":
            self.edit_entry_pass.config(show="")  # Show the password
            self.toggle_eye_button.config(image=self.eye_open_icon)  # Switch to open eye icon
        else:
            self.edit_entry_pass.config(show="*")  # Hide the password
            self.toggle_eye_button.config(image=self.eye_closed_icon)  # Switch to closed eye icon

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        self.folder_path_entry_save.delete(0, tk.END)  # Xóa nội dung trong entry trước khi cập nhật
        self.folder_path_entry_save.insert(0, folder_path)  # Thêm đường dẫn thư mục đã chọn vào entry

    def browse_file_video(self):
        filename = filedialog.askopenfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
        )
        
        self.file_path_video.delete(0, tk.END)
        self.file_path_video.insert(0, filename)
    def browse_file_frame(self):
        filename = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        
        self.file_path_frame.delete(0, tk.END)
        self.file_path_frame.insert(0, filename)
    def submit(self):
        try:
            # Đọc dữ liệu từ file JSON
            with open(self.file_path_frame.get(), "r") as f:
                frame_ = np.array(json.load(f), dtype=np.uint8)  # Đọc frame từ file JSON

            # Kiểm tra xem dữ liệu đọc vào có phải là một mảng hợp lệ hay không
            if frame_ is None or len(frame_.shape) != 3:  # Kiểm tra nếu frame không phải là một mảng 3 chiều
                self.log_display.add_log("Invalid frame data: Frame is None or not a 3D array.")
                return
            
            # Kiểm tra kích thước frame (đảm bảo frame có chiều cao, chiều rộng, và số kênh hợp lệ)
            if frame_.shape[0] == 0 or frame_.shape[1] == 0 or frame_.shape[2] != 3:  # Kiểm tra chiều cao, chiều rộng, và số kênh màu (3 kênh RGB)
                self.log_display.add_log("Invalid frame data: Invalid dimensions or color channels.")
                return
            
            # Nếu frame hợp lệ, tiếp tục với bước giải mã video
            self.decode_vid_data(frame_)

        except FileNotFoundError:
            self.log_display.add_log("File not found. Please check the file path.")
        except json.JSONDecodeError:
            self.log_display.add_log("Error decoding JSON data. The file may not be in valid JSON format.")
        except Exception as e:
            self.log_display.add_log(f"An unexpected error occurred: {str(e)}")

    def extract(self, frame,password):
        data_binary = ""
        final_decoded_msg = ""
        for i in frame:
            for pixel in i:
                r, g, b = binary.msgtobinary(pixel) 
                data_binary += r[-1]  
                data_binary += g[-1]  
                data_binary += b[-1]  
                total_bytes = [ data_binary[i: i+8] for i in range(0, len(data_binary), 8) ]
                decoded_data = ""
                for byte in total_bytes:
                    decoded_data += chr(int(byte, 2))
                    if decoded_data[-5:] == "*^*^*": 
                        for i in range(0,len(decoded_data)-5):
                            final_decoded_msg += decoded_data[i]

                        algorithm = CiperType.predict_cipher_type(final_decoded_msg)
                        if (algorithm == "XOR"):
                            final_decoded_msg = binary.xor_cipher(final_decoded_msg,password)
                        elif (algorithm == "Vigenère"):
                            final_decoded_msg = binary.vigenere_decrypt(final_decoded_msg,password)
                        else:      
                            final_decoded_msg = binary.rc4_decrypt(final_decoded_msg,password)


                        return  final_decoded_msg
            
    def decode_vid_data(self, frame_):
        password = self.edit_entry_pass.get()
        
        cap = cv2.VideoCapture(self.file_path_video.get())
        max_frame=0
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == False:
                break
            max_frame+=1
        print("Total number of Frame in selected Video :",max_frame)
        try:
            n = int(self.edit_entry_frame.get())
            if n > max_frame:
                self.log_display.add_log("Password must be less than or equal to "+max_frame)

        except ValueError:
            self.log_display.add_log("Please enter a valid integer for the password.")
            return  
        vidcap = cv2.VideoCapture(self.file_path_video.get())
        frame_number = 0
        result_message = ''
        while(vidcap.isOpened()):
            frame_number += 1
            ret, frame = vidcap.read()
            if ret == False:
                break
            if frame_number == n:
                result_message += self.extract(frame_,password)
        # lưu kq
        nameoffile = self.folder_path_entry_save.get() + "/" + self.new_txt.get()
        
        if not nameoffile.endswith(".txt"):
            nameoffile += ".txt"
        
        if os.path.exists(nameoffile):
            # Tên tệp đã tồn tại, thông báo cho người dùng
            self.log_display.add_log("File name already exists. Please choose another name.")
            return 0

        # Thêm mã hóa utf-8 khi ghi tệp
        try:
            with open(nameoffile, "w", encoding="utf-8") as output_file:
                output_file.write(result_message)
            self.log_display.add_log("File created successfully.")
        except UnicodeEncodeError as e:
            # Xử lý lỗi mã hóa
            self.log_display.add_log(f"Error while writing the file: {e}")
        return
