import tkinter as tk
from tkinter import filedialog
from binary import *
import cv2
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
        self.grid_rowconfigure(7, weight=0)
        self.grid_rowconfigure(8, weight=0)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        # Title Label with bold font for emphasis
        label = tk.Label(self, text="Image Encryption", font=("Arial", 18, "bold"), bg="white")
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
        lbl_image = tk.Label(self, text="Name New File:", bg="white", font=("Arial", 12))
        lbl_image.grid(row=6, column=0, padx=10, pady=10, sticky="e")
        self.new_image = ttk.Entry(self, width=30, font=("Arial", 12))
        self.new_image.grid(row=6, column=1, pady=10, sticky="we")

        # Submit Button
        submit_button = ttk.Button(self, text="Encode", command=self.submit, width=30)
        submit_button.grid(row=7, column=1, padx=10, pady=20, sticky="e")

        # Log Output Area
        self.log_label = tk.Label(self, text="", bg="white", font=("Arial", 10, "italic"))
        self.log_label.grid(row=8, column=0, padx=10, pady=5, sticky="e")

        #Log
        self.logger = Logger("app_log.txt")
        self.log_display = LogDisplay(self, self.logger)
        self.log_display.grid(row=8, column=0, columnspan=3, sticky="nsew")


    def toggle_password(self):
        try:
            # Toggle the password visibility
            if self.edit_entry_pass.cget("show") == "*":
                self.edit_entry_pass.config(show="")  # Show the password
                self.toggle_eye_button.config(image=self.eye_open_icon)  # Switch to open eye icon
            else:
                self.edit_entry_pass.config(show="*")  # Hide the password
                self.toggle_eye_button.config(image=self.eye_closed_icon)  # Switch to closed eye icon
        except Exception as e:
            self.log_display.add_log("Error" +" Error toggling password visibility: "+e)

    def browse_file(self):
        filename = filedialog.askopenfilename(
            defaultextension=".png", 
            filetypes=[
                ("All Image files", "*.jpeg;*.jpg;*.png"),
                ("JPEG files", "*.jpeg"),
                ("JPG files", "*.jpg"),
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ]
        )
        if filename:  # Only proceed if a file is selected
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, filename)
        else:
            self.log_display.add_log("No file selected.")

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:  # Only proceed if a folder is selected
            self.folder_path_entry_save.delete(0, tk.END)
            self.folder_path_entry_save.insert(0, folder_path)
        else:
            self.log_display.add_log("No folder selected.")

    def submit(self):
        try:
            # Construct the full image path for saving
            folder_path = self.folder_path_entry_save.get()
            new_file_name = self.new_image.get()
            
            if not folder_path or not new_file_name:
                self.log_display.add_log("Please specify a folder path and new file name.")

            full_image_path = folder_path + "/" + new_file_name
            if not full_image_path.endswith(".png"):
                full_image_path += ".png"

            image_path = self.file_path_entry.get()
            if not image_path:
                self.log_display.add_log("Please select an image file to encode.")
            image = cv2.imread(image_path)

            if image is None:
                self.log_display.add_log("Failed to load the selected image file.")
            
            # Perform encoding
            self.encode_img_data(image, full_image_path)
            self.log_display.add_log("Success", f"Data encoded and saved successfully at: {full_image_path}")
        except Exception as e:
            print("Error",e)
    def encode_img_data(self,img, output_path):
        message=self.edit_entry_text.get()    
        password=self.edit_entry_pass.get()
        totalData = len(message)+ len(password)
        if len(message) == 0: 
            self.log_display.add_log('Data entered to be encoded is empty')
        if len(password) == 0: 
            self.log_display.add_log('Data entered to be encoded is empty')

        no_of_bytes = (img.shape[0] * img.shape[1] * 3) // 8

        if totalData > no_of_bytes:
            self.log_display.add_log("Insufficient bytes Error, Need Bigger Image or give Less Data !!")
        
        algorithm = self.algorithm.get()
        data_hidden = ""
        if (algorithm == 0):
            data_hidden = binary.xor_cipher(message,password)+"*^*^*"
        elif (algorithm == 1):
            data_hidden = binary.vigenere_encrypt(message,password)+"*^*^*"
        else:      
            data_hidden = binary.rc4_encrypt(message,password)+"*^*^*"

        
        binary_data = binary.msgtobinary(data_hidden)

        length_data = len(binary_data)

        index_data = 0

        for i in img:
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

        cv2.imwrite(output_path, img)
        self.log_display.add_log("Encoded the data successfully in the Image and the image is successfully saved at:"+ output_path)
        return
# Kiểm tra
if __name__ == "__main__":
    root = tk.Tk()
    decode_component = EncodeComponent(root)
    decode_component.pack(fill="both", expand=True)
    root.mainloop()
