import customtkinter as ctk
from views.MainWindow import MainWindow

if __name__ == "__main__":
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")
    app = MainWindow()
    app.mainloop()