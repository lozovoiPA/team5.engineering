from tkinter import messagebox

import customtkinter as ctk
from datetime import timedelta

from dependencies import CollisionPrefs, NotificationPrefs


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent, collision_prefs: CollisionPrefs, notif_prefs: NotificationPrefs):
        super().__init__(parent)

        self.first_reminder_options = {
            "За 1 час": timedelta(hours=1),
            "За 40 минут": timedelta(minutes=40),
            "За 30 минут": timedelta(minutes=30)
        }
        self.second_reminder_options = {
            "За 15 минут": timedelta(minutes=15),
            "За 10 минут": timedelta(minutes=10),
            "За 5 минут": timedelta(minutes=5)
        }

        self.collision_prefs = collision_prefs
        self.notif_prefs = notif_prefs

        self.title("Настройки")
        self.geometry("500x550")
        self.resizable(False, False)

        self._build_ui()

    def _build_ui(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True)

        collision_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        collision_frame.pack(fill="x", padx=20, pady=10)

        collision_label = ctk.CTkLabel(
            collision_frame,
            text="Окно коллизии встреч:",
            font=ctk.CTkFont(size=14)
        )
        collision_label.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")

        time_input_frame = ctk.CTkFrame(collision_frame, fg_color="transparent")
        time_input_frame.grid(row=0, column=1, pady=5, sticky="w")

        self.collision_entry = ctk.CTkEntry(
            time_input_frame,
            width=80,
            height=30,
            font=ctk.CTkFont(size=14),
            placeholder_text="30"
        )
        self.collision_entry.pack(side="left", padx=(0, 5))
        self.collision_entry.insert(0, "30")

        self.collision_unit = ctk.CTkOptionMenu(
            time_input_frame,
            values=["минут", "часов"],
            width=80,
            height=30,
            font=ctk.CTkFont(size=14)
        )
        self.collision_unit.pack(side="left")

        hint_label = ctk.CTkLabel(
            collision_frame,
            text="(от 20 минут до 24 часов)",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        hint_label.grid(row=1, column=1, pady=(0, 5), sticky="w")

        separator1 = ctk.CTkFrame(main_frame, height=2, fg_color="gray")
        separator1.pack(fill="x", padx=20, pady=15)

        first_reminder_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        first_reminder_frame.pack(fill="x", padx=20, pady=10)

        first_reminder_label = ctk.CTkLabel(
            first_reminder_frame,
            text="Первое напоминание:",
            font=ctk.CTkFont(size=14)
        )
        first_reminder_label.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")

        self.first_reminder_combo = ctk.CTkOptionMenu(
            first_reminder_frame,
            values=list(self.first_reminder_options.keys()),
            width=150,
            height=35,
            font=ctk.CTkFont(size=14)
        )
        self.first_reminder_combo.grid(row=0, column=1, pady=5, sticky="w")
        self.first_reminder_combo.set("За 1 час")

        second_reminder_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        second_reminder_frame.pack(fill="x", padx=20, pady=10)

        second_reminder_label = ctk.CTkLabel(
            second_reminder_frame,
            text="Второе напоминание:",
            font=ctk.CTkFont(size=14)
        )
        second_reminder_label.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")

        self.second_reminder_combo = ctk.CTkOptionMenu(
            second_reminder_frame,
            values=list(self.second_reminder_options.keys()),
            width=150,
            height=35,
            font=ctk.CTkFont(size=14)
        )
        self.second_reminder_combo.grid(row=0, column=1, pady=5, sticky="w")
        self.second_reminder_combo.set("За 10 минут")

        separator2 = ctk.CTkFrame(main_frame, height=2, fg_color="gray")
        separator2.pack(fill="x", padx=20, pady=15)

        self.detailed_notifications = ctk.CTkCheckBox(
            main_frame,
            text="Расширенные уведомления",
            font=ctk.CTkFont(size=14),
            checkbox_width=22,
            checkbox_height=22,
            corner_radius=6
        )
        self.detailed_notifications.pack(pady=15)

        checkbox_hint = ctk.CTkLabel(
            main_frame,
            text="При включении показывать детальную информацию о встрече",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        checkbox_hint.pack(pady=(0, 10))

        save_btn = ctk.CTkButton(
            main_frame,
            text="Сохранить",
            command=self.save_settings,
            width=60,
            height=40,
            font=ctk.CTkFont(size=15),
            corner_radius=8
        )
        save_btn.pack(side='right', pady=(20, 20), padx=(0, 10))

        cancel_btn = ctk.CTkButton(
            main_frame,
            text="Отмена",
            command=self.destroy,
            width=60,
            height=40,
            font=ctk.CTkFont(size=15),
            corner_radius=8,
            fg_color="transparent", text_color="#000000", border_width=2,
            border_color="#cccccc", hover_color="#e0e0e0"
        )
        cancel_btn.pack(side='right', pady=(20, 20), padx=(0, 10))

    def get_collision_window_timedelta(self):
        try:
            value = int(self.collision_entry.get())
            unit = self.collision_unit.get()

            if unit == "минут":
                delta = timedelta(minutes=value)
            else:
                delta = timedelta(hours=value)

            min_delta = timedelta(minutes=20)
            max_delta = timedelta(hours=24)

            flag = delta < min_delta or delta > max_delta
            if flag:
                messagebox.showwarning("Ошибка",
                                       "Коллизия встреч указана неправильно.\nВведите значение от 20 минут до 24 часов.")
                return False
            return delta
        except ValueError:
            messagebox.showwarning("Ошибка", "Коллизия встреч указана неправильно.\nВведите значение от 20 минут до 24 часов.")
            return False

    def save_settings(self):
        delta = self.get_collision_window_timedelta()
        if isinstance(delta, timedelta):
            self.collision_prefs.collision_window = delta
            self.notif_prefs.first_notif_delta = self.first_reminder_options[self.first_reminder_combo.get()]
            self.notif_prefs.second_notif_delta = self.second_reminder_options[self.second_reminder_combo.get()]
            self.notif_prefs.short_notif = self.detailed_notifications.get()

            self.destroy()
