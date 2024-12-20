import tkinter as tk
from tkinter import filedialog
from binary import *
import cv2
import os
from tkinter import ttk
import tkinter
from PIL import Image, ImageTk
from CiperType import CiperType
from Logger import LogDisplay, Logger

class ImageInterface(tk.Frame):
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
        self.grid_rowconfigure(7, weight=0)
        self.grid_rowconfigure(8, weight=0)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        # Tiêu đề
        label = tk.Label(self, text="Image Decryption", font=("Arial", 18, "bold"), bg="white")
        label.grid(row=0, column=0, columnspan=3, padx=20, pady=20)
        # Button "Browse File" và Entry "File Path"
        lbl_browser_file = tk.Label(self, text="File Decrypt:", bg="white", font=("Arial", 10))
        lbl_browser_file.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.file_path_entry = ttk.Entry(self, width=50, font=("Arial", 10))
        self.file_path_entry.grid(row=1, column=1, pady=10, sticky="we")
        browse_button = ttk.Button(self, text="...", command=self.browse_file, width=5)
        browse_button.grid(row=1, column=2, padx=10, pady=10)

        # Password Entry
        lbl_pass = tk.Label(self, text="Password:", bg="white", font=("Arial", 10))
        lbl_pass.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.edit_entry_pass = ttk.Entry(self, width=30, font=("Arial", 12), show="*")
        self.edit_entry_pass.grid(row=2, column=1, pady=10, sticky="we")

        # Load eye icon images (open and closed)
        self.eye_open = Image.open("eye_open.png")  # Image for eye open
        self.eye_open = self.eye_open.resize((20, 20), Image.ANTIALIAS)
        self.eye_open_icon = ImageTk.PhotoImage(self.eye_open)
        self.eye_closed = Image.open("eye_close.png")  # Image for eye closed
        self.eye_closed = self.eye_closed.resize((20, 20), Image.ANTIALIAS)
        self.eye_closed_icon = ImageTk.PhotoImage(self.eye_closed)
        # Button to toggle password visibility
        self.toggle_eye_button = tk.Button(self, image=self.eye_closed_icon, bg="white", bd=0, command=self.toggle_password)
        self.toggle_eye_button.grid(row=2, column=2, padx=10)

        # Folder Path Save Entry
        lbl_browser_folder = tk.Label(self, text="Folder Path Save:", bg="white", font=("Arial", 10))
        lbl_browser_folder.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.folder_path_entry_save = ttk.Entry(self, width=50, font=("Arial", 10))
        self.folder_path_entry_save.grid(row=3, column=1, pady=10, sticky="we")
        browse_button_save = ttk.Button(self, text="...", command=self.browse_folder, width=5)
        browse_button_save.grid(row=3, column=2, padx=10, pady=10)

        # New File Name Entry
        lbl_txt = tk.Label(self, text="Name New File:", bg="white", font=("Arial", 10))
        lbl_txt.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.new_txt = ttk.Entry(self, width=30, font=("Arial", 10))
        self.new_txt.grid(row=4, column=1, pady=10, sticky="we")

        # Submit Button with hover effect
        submit_button = ttk.Button(self, text="Encode", command=self.submit, width=30)
        submit_button.grid(row=5, column=1, padx=10, pady=20, sticky="e")

        #Log
        self.logger = Logger("app_log.txt")
        self.log_display = LogDisplay(self, self.logger)
        self.log_display.grid(row=6, column=0, columnspan=3, sticky="nsew")
        
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

    def browse_file(self):
        filename = filedialog.askopenfilename(defaultextension=".png", filetypes=[("All Image files", "*.jpeg;*.jpg;*.png"), ("JPEG files", "*.jpeg"), ("JPG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")])
        
        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(0, filename)

    def submit(self):
        image = cv2.imread(self.file_path_entry.get())
        self.decode_img_data(image)


    def reserve_img_data(self, img):
        data_binary = ""
        for i in img:
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
                        decoded_data = decoded_data[:-5]
                        return decoded_data

    def decode_img_data(self,img):
        password=self.edit_entry_pass.get()
        decoded_data = self.reserve_img_data(img)
        algorithm = CiperType.predict_cipher_type(decoded_data)
        hidden_message = ""
        if (algorithm == "XOR"):
            hidden_message = binary.xor_cipher(decoded_data,password)
        elif (algorithm == "Vigenère"):
            hidden_message = binary.vigenere_decrypt(decoded_data,password)
        else:      
            hidden_message = binary.rc4_decrypt(decoded_data,password)

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
                output_file.write(hidden_message)
            self.log_display.add_log("File created successfully.")
        except UnicodeEncodeError as e:
            # Xử lý lỗi mã hóa
            self.log_display.add_log(f"Error while writing the file: {e}")
