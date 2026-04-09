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

            def shutdown():
                app.shutdown(None, None)

            def background_work():
                app.notif_worker.send_notification(sys.argv[2],
                                                   lambda args: app.root.after(0, shutdown),
                                                   lambda args: app.root.after(0, shutdown)
                                                   )
            threading.Thread(target=background_work).start()

    app.root.after(100, lambda: None)
    app.root.mainloop()
