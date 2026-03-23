import tkinter as tk
import threading
import keyboard
import sys
from services.screen_text_listener import ScreenTextListener

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        
        self.text_listener = ScreenTextListener()
        threading.Thread(target=self.program_exit).start() # по сути потом не будет, но пока чтобы можно было закрыть в консоли

        # вместо этого ниже подставляем ModelWorker
        self.text_listener.launch(self.print_text)

    def print_text(self, text):
        print(text[0:300])

    def program_exit(self):
        try:
            keyboard.wait('esc')
        except KeyboardInterrupt:
            pass
        finally:
            self.root.after(0, self.program_shutdown)

    def program_shutdown(self):
        print("App shutting down.")
        keyboard.unhook_all()
        self.text_listener.stop()
        self.root.destroy()

if __name__ == "__main__":
    app = App()
    print("App started.")

    app.root.mainloop()
    
