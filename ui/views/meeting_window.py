import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta

from data.entities.meeting import Meeting
from data.repositories.meeting_repository import MeetingRepository
from ui.view_models.meeting_window_view_model import MeetingWindowViewModel


class MeetingWindow(ctk.CTkToplevel):
    def __init__(self, parent, on_save, repository: MeetingRepository, prefill_meeting=None, on_cancel=None):
        super().__init__(parent)

        self.on_save = on_save
        self.on_cancel = lambda: self.destroy() if on_cancel is None else on_cancel
        self.prefill_meeting = prefill_meeting

        self.view_model = MeetingWindowViewModel(repository)

        self.is_edit_mode = (
                prefill_meeting is not None and
                hasattr(prefill_meeting, 'id') and
                prefill_meeting.id is not None and
                prefill_meeting.id > 0
        )
        if self.is_edit_mode:
            self.view_model.meeting = prefill_meeting
        else:
            self.view_model.meeting = Meeting()
        self.meeting = self.view_model.meeting

        if self.is_edit_mode:
            self.title("Редактирование встречи")
        else:
            self.title("Создание встречи")

        self.geometry("460x480")
        self.resizable(False, False)
        self.grab_set()

        self._build_ui()

        if self.prefill_meeting:
            self._prefill_form()
        else:
            self._set_default_datetime()

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color="#f0f0f0", corner_radius=0, height=50)
        header.pack(fill="x")

        if self.is_edit_mode:
            header_text = "Редактирование встречи"
        else:
            header_text = "Создание встречи"

        ctk.CTkLabel(header, text=header_text, font=ctk.CTkFont(size=17, weight="normal"),
                     text_color="#333333").pack(pady=12)

        ctk.CTkLabel(self, text="Название").pack(anchor="w", padx=32, pady=(24, 4))
        self.title_entry = ctk.CTkEntry(self, width=380, height=40)
        self.title_entry.pack(padx=32)
        self.title_entry.insert(0, "Встреча")

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

        self.dd = ctk.CTkEntry(date_row, width=60, height=40)
        self.dd.pack(side="left")
        ctk.CTkLabel(date_row, text=".").pack(side="left", padx=6)
        self.mm = ctk.CTkEntry(date_row, width=60, height=40)
        self.mm.pack(side="left")
        ctk.CTkLabel(date_row, text=".").pack(side="left", padx=6)
        self.yyyy = ctk.CTkEntry(date_row, width=100, height=40)
        self.yyyy.pack(side="left")

        time_block = ctk.CTkFrame(dt_frame, fg_color="transparent")
        time_block.pack(side="left")

        ctk.CTkLabel(time_block, text="Время").pack(anchor="w")
        self.time_entry = ctk.CTkEntry(time_block, width=120, height=40)
        self.time_entry.pack(pady=(4, 0))

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(side="right", padx=32, pady=(32, 24))

        self.cancel_btn: ctk.CTkButton = ctk.CTkButton(btn_frame, text="Отмена", width=110, height=40,
                                                       fg_color="transparent", text_color="#666666", border_width=2,
                                                       border_color="#cccccc", command=self.on_cancel)
        self.cancel_btn.pack(side="left", padx=(0, 12))

        button_text = "Сохранить" if self.is_edit_mode else "Создать"
        self.save_btn: ctk.CTkButton = ctk.CTkButton(btn_frame, text=button_text, width=110, height=40,
                                                     fg_color="#0066cc", hover_color="#0055aa", text_color="white",
                                                     command=self._try_save)
        self.save_btn.pack(side="left")

    def _set_default_datetime(self):
        """Устанавливаем текущую дату и время +1 час"""
        now = datetime.now()
        default_time = now + timedelta(hours=1)

        minutes = default_time.minute
        rounded_minutes = (minutes // 5) * 5
        if rounded_minutes == 60:
            rounded_minutes = 0
            default_time = default_time + timedelta(hours=1)

        default_time = default_time.replace(minute=rounded_minutes, second=0, microsecond=0)

        self.dd.delete(0, ctk.END)
        self.dd.insert(0, f"{default_time.day:02d}")
        self.mm.delete(0, ctk.END)
        self.mm.insert(0, f"{default_time.month:02d}")
        self.yyyy.delete(0, ctk.END)
        self.yyyy.insert(0, f"{default_time.year}")

        self.time_entry.delete(0, ctk.END)
        self.time_entry.insert(0, default_time.strftime("%H:%M"))

    def _prefill_form(self):
        self.title_entry.delete(0, ctk.END)
        self.title_entry.insert(0, self.prefill_meeting.title[:60])

        self.desc_entry.delete(0, ctk.END)
        self.desc_entry.insert(0, self.prefill_meeting.description)

        if '.' in self.prefill_meeting.date:
            parts = self.prefill_meeting.date.split('.')
            if len(parts) == 3:
                self.dd.delete(0, ctk.END)
                self.dd.insert(0, parts[0])
                self.mm.delete(0, ctk.END)
                self.mm.insert(0, parts[1])
                self.yyyy.delete(0, ctk.END)
                self.yyyy.insert(0, parts[2])

        self.time_entry.delete(0, ctk.END)
        self.time_entry.insert(0, self.prefill_meeting.time)

    def _try_save(self):
        def unblock_buttons():
            self.cancel_btn.configure(state="normal")
            self.save_btn.configure(state="normal", text="Сохранить" if self.is_edit_mode else "Создать")

        print(type(self.cancel_btn), type(self.save_btn))

        self.cancel_btn.configure(state="disabled")
        self.save_btn.configure(state="disabled", text="Сохранение...")

        title = self.title_entry.get().strip()
        if not title:
            messagebox.showwarning("Ошибка", "Введите название встречи")
            return

        date_str = f"{self.dd.get().strip()}.{self.mm.get().strip()}.{self.yyyy.get().strip()}"
        time_str = self.time_entry.get().strip()

        self.meeting.title = title
        self.meeting.date = date_str
        self.meeting.time = time_str
        self.meeting.description = self.desc_entry.get().strip()

        # Проверка коллизий (через вьюмодель)
        # Если есть коллизия (окно - 1 час) - вывод в логи
        collision_meetings = self.view_model.check_collisions()
        if collision_meetings is not None:
            messagebox.showwarning("Ошибка", "Обнаружены коллизии встреч, встреча не создана (пока).")
            unblock_buttons()
        else:
            if self.view_model.save_meeting():
                self.on_save(self.meeting)
                self.destroy()
            else:
                messagebox.showwarning("Ошибка", "Ошибка при сохранении встречи. Не удалось сохранить.")
                unblock_buttons()
