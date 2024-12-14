import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from binary import *

class TextEncoderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Encoder")
        self.root.geometry("600x400")

        self.algorithm = tk.IntVar(value=0)
        self.input_file = None
        self.output_file = None

        # Layout
        self.create_widgets()

    def create_widgets(self):
        # Input File Section
        ttk.Label(self.root, text="Input File:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.input_file_entry = ttk.Entry(self.root, width=50)
        self.input_file_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        ttk.Button(self.root, text="Browse", command=self.browse_input_file).grid(row=0, column=2, padx=10, pady=10)

        # Output File Section
        ttk.Label(self.root, text="Output File:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.output_file_entry = ttk.Entry(self.root, width=50)
        self.output_file_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        ttk.Button(self.root, text="Browse", command=self.browse_output_file).grid(row=1, column=2, padx=10, pady=10)

        # Password Section
        ttk.Label(self.root, text="Password:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.password_entry = ttk.Entry(self.root, show="*", width=50)
        self.password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.show_password = tk.BooleanVar(value=False)
        self.toggle_password_btn = ttk.Checkbutton(
            self.root, text="Show", variable=self.show_password, command=self.toggle_password_visibility
        )
        self.toggle_password_btn.grid(row=2, column=2, padx=10, pady=10)

        # Algorithm Selection
        ttk.Label(self.root, text="Algorithm:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        algorithms = ["XOR", "Vigenere", "RC4"]
        for i, algo in enumerate(algorithms):
            ttk.Radiobutton(self.root, text=algo, variable=self.algorithm, value=i).grid(row=3, column=i + 1, padx=10, pady=10, sticky="w")

        # Log Display
        ttk.Label(self.root, text="Log:").grid(row=4, column=0, padx=10, pady=10, sticky="nw")
        self.log_display = tk.Text(self.root, height=10, width=70, state="disabled")
        self.log_display.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky="w")

        # Action Buttons
        ttk.Button(self.root, text="Submit", command=self.submit).grid(row=5, column=1, pady=20)

    def browse_input_file(self):
        self.input_file = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        self.input_file_entry.delete(0, tk.END)
        self.input_file_entry.insert(0, self.input_file)

    def browse_output_file(self):
        self.output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        self.output_file_entry.delete(0, tk.END)
        self.output_file_entry.insert(0, self.output_file)

    def toggle_password_visibility(self):
        if self.show_password.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def log(self, message):
        self.log_display.config(state="normal")
        self.log_display.insert(tk.END, message + "\n")
        self.log_display.config(state="disabled")

    def encode_txt_data(self, text, password, algorithm):
        if algorithm == 0:
            return xor_cipher(text, password)
        elif algorithm == 1:
            return vigenere_encrypt(text, password)
        elif algorithm == 2:
            return rc4_encrypt(text, password)

    def submit(self):
        input_file = self.input_file_entry.get()
        output_file = self.output_file_entry.get()
        password = self.password_entry.get()

        if not input_file or not output_file or not password:
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        if not os.path.exists(input_file):
            messagebox.showerror("Error", "Input file does not exist!")
            return

        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()

        algorithm = self.algorithm.get()
        encoded_text = self.encode_txt_data(text, password, algorithm)

        if len(encoded_text) > 10000:
            self.log("Encoded text is too long. Please reduce input size.")
            return

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(encoded_text)

        self.log(f"File encoded successfully and saved to {output_file}.")
        messagebox.showinfo("Success", "Encoding completed successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEncoderApp(root)
    root.mainloop()
