import customtkinter as ctk

from data.entities.meeting import Meeting


class MeetingInfoWindow(ctk.CTkToplevel):
    def __init__(self, parent, meeting: Meeting, on_close):
        super().__init__(parent)
        self.meeting = meeting
        self.on_close = on_close

        self.geometry("460x480")
        self.resizable(False, False)

        self.title(f"{meeting.title}")

        self._build_ui()

    def _build_ui(self):
        main_frame = ctk.CTkFrame(self, corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        title_label = ctk.CTkLabel(
            main_frame,
            text=f"📅 Ваша встреча скоро начнется",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 10))

        meeting_title_label = ctk.CTkLabel(
            main_frame,
            text=f"{self.meeting.title}",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        meeting_title_label.pack(pady=(10, 5))

        description_label = ctk.CTkLabel(
            main_frame,
            text=self.meeting.description,
            font=ctk.CTkFont(size=14),
            wraplength=350,
            justify="center"
        )
        description_label.pack(pady=(5, 10))

        separator = ctk.CTkFrame(main_frame, height=2, fg_color="gray")
        separator.pack(fill="x", padx=20, pady=10)

        time_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        time_frame.pack(pady=5)

        date_label = ctk.CTkLabel(
            time_frame,
            text="📆 Дата:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        date_label.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")

        date_value = ctk.CTkLabel(
            time_frame,
            text=self.meeting.date,
            font=ctk.CTkFont(size=16)
        )
        date_value.grid(row=0, column=1, pady=5, sticky="w")

        # Time
        time_label = ctk.CTkLabel(
            time_frame,
            text="🕐 Время:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        time_label.grid(row=1, column=0, padx=(0, 10), pady=5, sticky="w")

        time_value = ctk.CTkLabel(
            time_frame,
            text=self.meeting.time,
            font=ctk.CTkFont(size=16)
        )
        time_value.grid(row=1, column=1, pady=5, sticky="w")

        ok_button = ctk.CTkButton(
            main_frame,
            text="OK",
            command=self.on_close,
            width=120,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=8
        )
        ok_button.pack(pady=(30, 20))
