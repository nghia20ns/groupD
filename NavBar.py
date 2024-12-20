import tkinter as tk
from Interface.TextInterface.TextInterface import TextInterface
from Interface.ImageInterface.ImageInterface import ImageInterface
from Interface.AudioInterface.AudioInterface import AudioInterface
from Interface.VideoInterface.VideoInterface import VideoInterface
from Interface.DecryptionInterface.DecryptionInterface import DecryptionInterface

class Navbar(tk.Frame):
    def __init__(self, master, state, update_state_func):
        super().__init__(master, bg="#f0f0f5", bd=2, relief="groove")  # Lighter background color
        self.master = master
        self.state = state
        self.update_state = update_state_func

        # Add logo to navbar
        self.add_logo()

        # Create buttons
        self.buttons = []
        self.create_button("Text Steganography", TextInterface, 1)
        self.create_button("Image Steganography", ImageInterface, 2)
        self.create_button("Audio Steganography", AudioInterface, 3)
        self.create_button("Video Steganography", VideoInterface, 4)
        self.create_button("Decryption With AI", DecryptionInterface, 5)

    def add_logo(self):
        try:
            logo = tk.PhotoImage(file="Images/logo.png")
            logo_label = tk.Label(self, image=logo, bg="#f0f0f5")  # Matching background color
            logo_label.image = logo
            logo_label.grid(row=0, column=0, pady=10, padx=10, sticky="n")
        except Exception as e:
            print(f"Could not load logo: {e}")

    def create_button(self, text, interface, row_idx):
        button = tk.Button(self, text=text, command=lambda: self.switch_interface(interface),
                        bg="#f0f8ff", font=("Helvetica", 10), relief="solid", borderwidth=1, 
                        highlightthickness=0, cursor="hand2", state=tk.NORMAL, height=2, width=20)
        
        # Adding rounded corners (only for tkinter 8.6 and above)
        button.config(highlightbackground="#f0f8ff", highlightcolor="#f0f8ff", bd=0)
        button.grid(row=row_idx, column=0, sticky="ew", padx=10, pady=5)
        self.add_hover_effect(button)
        self.buttons.append((button, interface))

    def add_hover_effect(self, widget):
        def on_enter(event):
            if widget['bg'] not in ("#99ddff", "#f0f0f5"):  # Avoid hover effect on selected button
                widget['bg'] = "#a9c9f5"  # Subtle light blue hover effect
        def on_leave(event):
            if widget['bg'] not in ("#99ddff", "#f0f0f5"):
                widget['bg'] = "#f0f8ff"  # Restore button color
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def switch_interface(self, interface):
        if self.state == interface:
            return
        self.update_state(interface)
        self.highlight_selected_button(interface)

    def highlight_selected_button(self, selected_interface):
        for button, iface in self.buttons:
            if iface == selected_interface:
                button.config(bg="#99ddff", state=tk.DISABLED, font=("Helvetica", 10))  # Active button with accent color
            else:
                button.config(bg="#f0f8ff", state=tk.NORMAL, font=("Helvetica", 10))  # Reset other buttons
