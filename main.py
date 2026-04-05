import customtkinter as ctk
from app import App

app = None

if __name__ == "__main__":
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")
    
    app = App()
    app.launch()

    app.root.after(100, lambda: None)
    app.root.mainloop()
