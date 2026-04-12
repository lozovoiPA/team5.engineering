import os
import signal
import sys
import threading

import customtkinter as ctk
from app import App
from data.entities.notification import Notification

app = None

if __name__ == "__main__":
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")
    
    app = App()

    if len(sys.argv) == 1:
        app.init()
        app.launch()
    else:
        if sys.argv[1] == "--send-notif" and len(sys.argv) == 3:
            app.handle_notification(sys.argv[2])

    app.root.after(100, lambda: None)
    app.root.mainloop()
