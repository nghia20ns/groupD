import tkinter as tk
from tkinter import filedialog
from binary import *
import os
import wave

from tkinter import ttk
import tkinter
from PIL import Image, ImageTk
from Logger import LogDisplay, Logger

class DecodeComponent(tk.Frame):
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
        label = tk.Label(self, text="Audio Decryption", font=("Arial", 18, "bold"), bg="white")
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
        self.edit_entry_pass = ttk.Entry(self, width=30, font=("Arial", 10), show="*")
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


        #Radio Button encryption algorithm
        lbl_text = tk.Label(self, text="Decryption algorithm:", bg="white", font=("Arial", 10))
        lbl_text.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        # Frame cho các nút RadioButton
        self.buttons_frame = tkinter.Frame(self, bg="white")
        self.buttons_frame.grid(row=3, column=1, pady=10)
        # Các tùy chọn cho RadioButton
        status_options = ["XOR Cipher", "Vigenère Cipher", "RC4"]
        self.algorithm = tk.IntVar()
        # Tạo các nút RadioButton
        for index in range(len(status_options)):
            radio_button = tk.Radiobutton(
                self.buttons_frame,
                text=status_options[index],
                variable=self.algorithm,
                value=index,
                padx=5,
                font=("Arial", 9),  # Chỉnh sửa font chữ và kích thước
                bg="white"        # Chỉnh sửa màu nền
            )
            radio_button.grid(row=0, column=index, padx=5)  # Chia đều các cột cho các nút radio

        # Folder Path Save Entry
        lbl_browser_folder = tk.Label(self, text="Folder Path Save:", bg="white", font=("Arial", 10))
        lbl_browser_folder.grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.folder_path_entry_save = ttk.Entry(self, width=50, font=("Arial", 10))
        self.folder_path_entry_save.grid(row=5, column=1, pady=10, sticky="we")
        browse_button_save = ttk.Button(self, text="...", command=self.browse_folder, width=5)
        browse_button_save.grid(row=5, column=2, padx=10, pady=10)

        # New File Name Entry
        lbl_txt = tk.Label(self, text="Name New File:", bg="white", font=("Arial", 10))
        lbl_txt.grid(row=6, column=0, padx=10, pady=10, sticky="e")
        self.new_txt = ttk.Entry(self, width=30, font=("Arial", 10))
        self.new_txt.grid(row=6, column=1, pady=10, sticky="we")

        # Submit Button with hover effect
        submit_button = ttk.Button(self, text="Encode", command=self.submit, width=30)
        submit_button.grid(row=7, column=1, padx=10, pady=20, sticky="e")

        # Log Output Area
        self.log_label = tk.Label(self, text="", bg="white", font=("Arial", 10, "italic"))
        self.log_label.grid(row=8, column=1, padx=10, pady=5, sticky="e")
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
        try:
            folder_path = filedialog.askdirectory()
            if folder_path:
                self.folder_path_entry_save.delete(0, tk.END)
                self.folder_path_entry_save.insert(0, folder_path)
            else:
                self.log_display.add_log("No folder selected.")
        except Exception as e:
            self.log_display.add_log(f"Error selecting folder: {e}")

    def browse_file(self):
        filename = filedialog.askopenfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav"), ("All files", "*.*")])
        
        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(0, filename)

    def submit(self):
        if not self.file_path_entry.get():
            self.log_display.add_log("Please select a file to decrypt.")
            return
        if not self.folder_path_entry_save.get():
            self.log_display.add_log("Please select a folder to save the file.")
            return
        if not self.new_txt.get().strip():
            self.log_display.add_log("Please enter a valid name for the new file.")
            return
        try:
            self.decode_audio_data()
        except Exception as e:
            self.log_display.add_log(f"Error during decoding: {e}")

    def reserve_audio_data(self, frame_bytes):
        extracted = ""
        p=0
        for i in range(len(frame_bytes)):
            if(p==1):
                break
            res = bin(frame_bytes[i])[2:].zfill(8)
            if res[len(res)-2]==0:
                extracted+=res[len(res)-4]
            else:
                extracted+=res[len(res)-1]
        
            all_bytes = [ extracted[i: i+8] for i in range(0, len(extracted), 8) ]
            decoded_data = ""
            for byte in all_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-5:] == "*^*^*":
                    return decoded_data[:-5]  

    def decode_audio_data(self):
        song = wave.open(self.file_path_entry.get(), mode='rb')

        nframes=song.getnframes()
        frames=song.readframes(nframes)
        frame_list=list(frames)
        frame_bytes=bytearray(frame_list)

        password=self.edit_entry_pass.get()
        result = self.reserve_audio_data(frame_bytes)
        algorithm = self.algorithm.get()
        hidden_message = ""
        if (algorithm == 0):
            hidden_message = binary.xor_cipher(result,password)
        elif (algorithm == 1):
            hidden_message = binary.vigenere_decrypt(result,password)
        else:      
            hidden_message = binary.rc4_decrypt(result,password)


        nameoffile = self.folder_path_entry_save.get() + "/" + self.new_txt.get()
        if not nameoffile.endswith(".txt"):
            nameoffile += ".txt"
        if os.path.exists(nameoffile):
            # Tên tệp đã tồn tại, thông báo cho người dùng
            self.log_display.add_log("File name already exists. Please choose another name.")
            return 0
        with open(nameoffile, "w", encoding="utf-8") as output_file:
            output_file.write(hidden_message)
            self.log_display.add_log("create file successful.")

        return
