import tkinter as tk
from Interface.TextInterface.TextInterface import TextInterface
from Interface.ImageInterface.ImageInterface import ImageInterface
from Interface.AudioInterface.AudioInterface import AudioInterface
from Interface.VideoInterface.VideoInterface import VideoInterface
from Interface.DecryptionInterface.DecryptionInterface import DecryptionInterface
class Navbar(tk.Frame):
    def __init__(self, master, state, update_state_func):
        super().__init__(master, bg="#f0f8ff", bd=2, relief="groove")
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
            logo_label = tk.Label(self, image=logo, bg="#cceeff")
            logo_label.image = logo
            logo_label.grid(row=0, column=0, pady=10, padx=10, sticky="n")
        except Exception as e:
            print(f"Could not load logo: {e}")

    def create_button(self, text, interface, row_idx):
        button = tk.Button(self, text=text, command=lambda: self.switch_interface(interface),
                           bg="#e6f7ff", font=("Helvetica", 11), relief="flat", cursor="hand2")
        button.grid(row=row_idx, column=0, sticky="ew", padx=10, pady=5)
        self.add_hover_effect(button)
        self.buttons.append((button, interface))

    def add_hover_effect(self, widget):
        def on_enter(event):
            if widget['bg'] not in ("#66ccff", "#66b3ff"):
                widget['bg'] = "#99ddff"
        def on_leave(event):
            if widget['bg'] not in ("#66ccff", "#66b3ff"):
                widget['bg'] = "#e6f7ff"
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
                button['bg'] = "#66ccff"
                button['relief'] = "sunken"
            else:
                button['bg'] = "#e6f7ff"
                button['relief'] = "flat"
