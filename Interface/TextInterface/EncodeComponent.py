import tkinter as tk
from tkinter import filedialog
from binary import *
import os
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
        label = tk.Label(self, text="Text Encryption", font=("Arial", 18, "bold"), bg="white")
        label.grid(row=0, column=0, columnspan=3, padx=20, pady=20)

        # Text Entry
        lbl_text = tk.Label(self, text="Text to encrypt:", bg="white", font=("Arial", 12))
        lbl_text.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.edit_entry_text = ttk.Entry(self, width=30, font=("Arial", 12))
        self.edit_entry_text.grid(row=1, column=1, pady=10, sticky="we")

        # Password Entry
        lbl_pass = tk.Label(self, text="Password:", bg="white", font=("Arial", 12))
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

        # Radio Button encryption algorithm
        lbl_text = tk.Label(self, text="Encryption algorithm:", bg="white", font=("Arial", 12))
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
                font=("Arial", 10),  # Adjust font size
                bg="white"        # Adjust background color
            )
            radio_button.grid(row=0, column=index, padx=5)

        # File Path Entry
        lbl_browser_file = tk.Label(self, text="File Encode:", bg="white", font=("Arial", 12))
        lbl_browser_file.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.file_path_entry = ttk.Entry(self, width=50, font=("Arial", 12))
        self.file_path_entry.grid(row=4, column=1, pady=10, sticky="we")
        browse_button = ttk.Button(self, text="...", command=self.browse_file, width=5)
        browse_button.grid(row=4, column=2, padx=10, pady=10)

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
        filename = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(0, filename)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        self.folder_path_entry_save.delete(0, tk.END)  # Xóa nội dung trong entry trước khi cập nhật
        self.folder_path_entry_save.insert(0, folder_path)  # Thêm đường dẫn thư mục đã chọn vào entry

    def submit(self):
        try:
            # Kiểm tra file đầu vào
            input_file = self.file_path_entry.get()
            if not os.path.exists(input_file):
                self.log_display.add_log("Error: Input file not found or inaccessible.")
                return
            
            # Kiểm tra folder đầu ra
            output_folder = self.folder_path_entry_save.get()
            if not os.path.exists(output_folder):
                self.log_display.add_log("Error: Output folder path does not exist.")
                return
            
            # Kiểm tra tên file đầu ra
            output_file = os.path.join(output_folder, self.new_txt.get())
            if not output_file.endswith(".txt"):
                output_file += ".txt"
            if os.path.exists(output_file):
                self.log_display.add_log("Error: File name already exists. Please choose another name.")
                return
            
            # Kiểm tra mật khẩu
            password = self.edit_entry_pass.get()
            if not password:
                self.log_display.add_log("Error: Password cannot be empty.")
                return
            
            # Kiểm tra thuật toán
            algorithm = self.algorithm.get()
            if algorithm == 0:
                self.log_display.add_log("Error: Invalid encryption algorithm selected.")
                return
            
            # Tiến hành mã hóa
            check = self.encode_txt_data()
            if check == 0:
                self.log_display.add_log("Error: Encoding failed.")
            else:
                self.log_display.add_log(f"Create successful! File saved in {output_file}")
        except Exception as e:
            self.log_display.add_log(f"An unexpected error occurred: {str(e)}")

    def encode_txt_data(self):
        count2=0
        file1 = open(self.file_path_entry.get(),"r",encoding="utf-8")
        for line in file1: 
            for word in line.split():
                count2=count2+1
        file1.close()       
        bt=int(count2)
        message=self.edit_entry_text.get()
        password=self.edit_entry_pass.get()
        algorithm = self.algorithm.get()
        clipertext = ""
        if (algorithm == 0):
            clipertext = binary.xor_cipher(message,password)
        elif (algorithm == 1):
            clipertext = binary.vigenere_encrypt(message,password)
        else:      
            clipertext = binary.rc4_encrypt(message,password)

        l=len(clipertext)
        if(l<=bt):
            self.txt_encode(clipertext)
        else:
            self.log_display.add_log("Create Failed! String is too big please reduce string size")
            return 0

    def txt_encode(self,text):
        l=len(text)
        i=0
        add=''
        print("Length of binary after conversion:- ", l)

        while i<l:
            t=ord(text[i])
            if(t>=32 and t<=64):
                t1=t+48
                t2=t1^170       #170: 10101010
                res = bin(t2)[2:].zfill(8)
                add+="0011"+res
            
            else:
                t1=t-48
                t2=t1^170
                res = bin(t2)[2:].zfill(8)
                add+="0110"+res
            i+=1
        res1 =add + "111111111111"
        length = len(res1)

        print("Length of binary after conversion:- ",length)

        HM_SK=""
        ZWC={"00":u'\u200C',"01":u'\u202C',"11":u'\u202D',"10":u'\u200E'}      
        file1 = open(self.file_path_entry.get(),"r+")
        nameoffile = self.folder_path_entry_save.get() + "/" + self.new_txt.get()
        if not nameoffile.endswith(".txt"):
            nameoffile += ".txt"
        if os.path.exists(nameoffile):
            # Tên tệp đã tồn tại, thông báo cho người dùng
            self.log_display.add_log("File name already exists. Please choose another name.")
            return 0
        with open(nameoffile, "w+", encoding="utf-8") as file3:
            word = []
            for line in file1:
                word += line.split()
            i = 0
            while i < len(res1):  
                s = word[int(i / 12)]
                j = 0
                HM_SK = ""
                while j < 12:
                    if i + j + 1 >= len(res1):  # Kiểm tra nếu chỉ số vượt giới hạn
                        self.log_display.add_log("Number of characters exceeded limit, please re-enter information or change to another encoding type.")
                        return 0
                    x = res1[j + i] + res1[i + j + 1]
                    if x in ZWC:
                        HM_SK += ZWC[x]
                    else:
                        self.log_display.add_log("Warning: Key "+x+" is not valid in ZWC.")
                        HM_SK += ''  # Bỏ qua hoặc thêm xử lý khác nếu cần
                    j += 2
                s1 = s + HM_SK
                file3.write(s1 + " ")
                i += 12
            t = int(len(res1) / 12)
            while t < len(word):
                file3.write(word[t] + " ")
                t += 1
        file3.close()  
        file1.close()

if __name__ == "__main__":
    
    root = tk.Tk()
    encode_component = EncodeComponent(root, None)
    encode_component.pack(fill="both", expand=True)
    root.mainloop()