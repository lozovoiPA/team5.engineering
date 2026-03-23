import customtkinter as ctk
from tkinter import messagebox
from entities.Meeting import Meeting


class MeetingWindow(ctk.CTkToplevel):
    def __init__(self, parent, on_create):
        super().__init__(parent)
        self.title("Создание встречи")
        self.geometry("460x480")
        self.resizable(False, False)
        self.grab_set()
        self.on_create = on_create

        self._build_ui()

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color="#f0f0f0", corner_radius=0, height=50)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="Создание встречи", font=ctk.CTkFont(size=17, weight="normal"),
                     text_color="#333333").pack(pady=12)

        ctk.CTkLabel(self, text="Название").pack(anchor="w", padx=32, pady=(24, 4))
        self.title_entry = ctk.CTkEntry(self, width=380, height=40)
        self.title_entry.pack(padx=32)
        self.title_entry.insert(0, "Аксенов")

        ctk.CTkLabel(self, text="Описание").pack(anchor="w", padx=32, pady=(20, 4))
        self.desc_entry = ctk.CTkEntry(self, width=380, height=40)
        self.desc_entry.pack(padx=32, pady=(4, 24))

        dt_frame = ctk.CTkFrame(self, fg_color="transparent")
        dt_frame.pack(fill="x", padx=32, pady=12)

        date_block = ctk.CTkFrame(dt_frame, fg_color="transparent")
        date_block.pack(side="left", padx=(0, 40))

        ctk.CTkLabel(date_block, text="Дата").pack(anchor="w")
        date_row = ctk.CTkFrame(date_block, fg_color="transparent")
        date_row.pack(pady=(4, 0))

        self.dd = ctk.CTkEntry(date_row, width=60, height=40); self.dd.pack(side="left")
        ctk.CTkLabel(date_row, text=".").pack(side="left", padx=6)
        self.mm = ctk.CTkEntry(date_row, width=60, height=40); self.mm.pack(side="left")
        ctk.CTkLabel(date_row, text=".").pack(side="left", padx=6)
        self.yyyy = ctk.CTkEntry(date_row, width=100, height=40); self.yyyy.pack(side="left")

        self.dd.insert(0, "03")
        self.mm.insert(0, "03")
        self.yyyy.insert(0, "2026")

        time_block = ctk.CTkFrame(dt_frame, fg_color="transparent")
        time_block.pack(side="left")

        ctk.CTkLabel(time_block, text="Время").pack(anchor="w")
        self.time_entry = ctk.CTkEntry(time_block, width=120, height=40)
        self.time_entry.pack(pady=(4, 0))
        self.time_entry.insert(0, "12:25")

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(side="right", padx=32, pady=(32, 24))

        ctk.CTkButton(btn_frame, text="Отмена", width=110, height=40,
                      fg_color="transparent", text_color="#666666", border_width=2,
                      command=self.destroy).pack(side="left", padx=(0, 12))

        ctk.CTkButton(btn_frame, text="Создать", width=110, height=40,
                      command=self._try_create).pack(side="left")

    def _try_create(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showwarning("Ошибка", "Введите название встречи")
            return

        date_str = f"{self.dd.get().strip()}.{self.mm.get().strip()}.{self.yyyy.get().strip()}"
        time_str = self.time_entry.get().strip()

        meeting = Meeting(
            title=title,
            date=date_str,
            time=time_str,
            description=self.desc_entry.get().strip()
        )

        self.on_create(meeting)
        self.destroy()