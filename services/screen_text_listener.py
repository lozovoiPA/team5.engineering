import keyboard
import pyperclip
import pyautogui
import threading
import time

pyautogui.PAUSE = 0.1

class ScreenTextListener:
    def __init__(self):
        self.thread = None
        self.hotkey = 'alt+shift+z'
        self.pass_to = None

    def launch(self, f):
        keyboard.add_hotkey(self.hotkey, self.get_selected_text)
        self.pass_to = f
        
        self.thread = threading.Thread(target=self.listen, daemon=True)
        self.thread.start()

    def listen(self):
        keyboard.wait()

    def get_selected_text(self):
        original_clipboard = pyperclip.paste()

        time.sleep(0.1)
        with pyautogui.hold('ctrl'):
            time.sleep(0.1)
            pyautogui.press('c')

        selected_text = pyperclip.paste()
        print(len(selected_text))
        pyperclip.copy(original_clipboard)

        threading.Thread(target = self.pass_to(selected_text)).start()

    def stop(self):
        keyboard.unhook_all()
