import tkinter as tk
from tkinter import filedialog
import wave
import os 
from binary import *
from tkinter import ttk
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
        self.grid_rowconfigure(7, weight=0)
        self.grid_rowconfigure(8, weight=0)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        # Title Label with bold font for emphasis
        label = tk.Label(self, text="Audio Encryption", font=("Arial", 18, "bold"), bg="white")
        label.grid(row=0, column=0, columnspan=3, padx=20, pady=20)

        # Text Entry
        lbl_text = tk.Label(self, text="Text to encrypt:", bg="white", font=("Arial", 10))
        lbl_text.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.edit_entry_text = ttk.Entry(self, width=30, font=("Arial", 10))
        self.edit_entry_text.grid(row=1, column=1, pady=10, sticky="we")

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
        # Radio Button encryption algorithm
        lbl_text = tk.Label(self, text="Encryption algorithm:", bg="white", font=("Arial", 10))
        lbl_text.grid(row=3, column=0, padx=10, pady=10, sticky="e")

        # Frame for RadioButton options
        self.buttons_frame = tk.Frame(self, bg="white")
        self.buttons_frame.grid(row=3, column=1, pady=10)
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
                font=("Arial", 9),  # Adjust font size
                bg="white"        # Adjust background color
            )
            radio_button.grid(row=0, column=index, padx=5)



        # File Path Entry
        lbl_browser_file = tk.Label(self, text="File Encode:", bg="white", font=("Arial", 10))
        lbl_browser_file.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.file_path_entry = ttk.Entry(self, width=50, font=("Arial", 10))
        self.file_path_entry.grid(row=4, column=1, pady=10, sticky="we")
        browse_button = ttk.Button(self, text="...", command=self.browse_file, width=5)
        browse_button.grid(row=4, column=2, padx=10, pady=10)

        # Folder Path Save Entry
        lbl_browser_folder = tk.Label(self, text="Folder Path Save:", bg="white", font=("Arial", 10))
        lbl_browser_folder.grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.folder_path_entry_save = ttk.Entry(self, width=50, font=("Arial", 10))
        self.folder_path_entry_save.grid(row=5, column=1, pady=10, sticky="we")
        browse_button_save = ttk.Button(self, text="...", command=self.browse_folder, width=5)
        browse_button_save.grid(row=5, column=2, padx=10, pady=10)

        # New File Name Entry
        lbl_audio = tk.Label(self, text="Name New File:", bg="white", font=("Arial", 10))
        lbl_audio.grid(row=6, column=0, padx=10, pady=10, sticky="e")
        self.new_audio = ttk.Entry(self, width=30, font=("Arial", 10))
        self.new_audio.grid(row=6, column=1, pady=10, sticky="we")

        # Submit Button
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

    def browse_file(self):
        filename = filedialog.askopenfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav"), ("All files", "*.*")])
        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(0, filename)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        self.folder_path_entry_save.delete(0, tk.END)
        self.folder_path_entry_save.insert(0, folder_path)

    def submit(self):
    # Lấy thư mục và tên file
        folder_path = self.folder_path_entry_save.get()
        file_name = self.new_audio.get()

        # Kiểm tra xem người dùng có chọn thư mục lưu không
        if not folder_path:
            self.log_display.add_log("Please select a folder to save the file.")
            return
        
        # Kiểm tra tên file và thêm đuôi .wav nếu chưa có
        if not file_name.endswith(".wav"):
            file_name += ".wav"
        
        # Kết hợp đường dẫn đầy đủ
        full_audio_path = os.path.join(folder_path, file_name)

        # Tiến hành mã hóa và lưu file
        self.encode_aud_data(full_audio_path)
        self.log_display.add_log(f"Encoding completed successfully. File saved to: {full_audio_path}")


    def encode_aud_data(self, output_path):
        song = wave.open(self.file_path_entry.get(), mode='rb')
        nframes = song.getnframes()
        frames = song.readframes(nframes)
        frame_bytes = bytearray(frames)

        message = self.edit_entry_text.get()    
        password = self.edit_entry_pass.get()

        # Chuyển message và password sang nhị phân
        # data = password + '*' + message + '*^*^*'
        algorithm = self.algorithm.get()
        data_hidden = ""
        if (algorithm == 0):
            data_hidden = binary.xor_cipher(message,password)+"*^*^*"
        elif (algorithm == 1):
            data_hidden = binary.vigenere_encrypt(message,password)+"*^*^*"
        else:      
            data_hidden = binary.rc4_encrypt(message,password)+"*^*^*"

        print(data_hidden)

        result = ''.join([format(ord(c), '08b') for c in data_hidden])

        # Mã hóa từng bit vào frame_bytes
        for i in range(len(result)):
            frame_bytes[i] = (frame_bytes[i] & 254) | int(result[i])

        # Lưu lại file âm thanh đã mã hóa
        with wave.open(output_path, 'wb') as fd:
            fd.setparams(song.getparams())
            fd.writeframes(bytes(frame_bytes))
        song.close()

# Kiểm tra
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Audio Encoding Tool")
    encode_component = EncodeComponent(root)
    encode_component.pack(fill="both", expand=True)
    root.mainloop()
