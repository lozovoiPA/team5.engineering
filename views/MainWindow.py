import customtkinter as ctk
from tkinter import messagebox
from entities.Meeting import Meeting
from views.MeetingWindow import MeetingWindow


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Meeting Planner")
        self.geometry("860x620")
        self.minsize(720, 500)

        self.meetings = [
            Meeting("Встреча 1", "22.02.2026", "10:35"),
            Meeting("Встреча 2", "22.02.2026", "10:35"),
            Meeting("Встреча 3", "22.02.2026", "10:35"),
            Meeting("Встреча 4", "22.02.2026", "10:35"),
        ]

        self._build_ui()

    def _build_ui(self):
        top_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=0, height=56)
        top_frame.pack(fill="x")

        ctk.CTkLabel(top_frame, text="Meeting Planner", text_color="black",
                     font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold")) \
            .pack(side="left", padx=24, pady=12)

        btn_container = ctk.CTkFrame(top_frame, fg_color="transparent")
        btn_container.pack(side="right", padx=20, pady=10)

        ctk.CTkButton(btn_container, text="+ Создать встречу", width=160, height=36,
                      corner_radius=8, hover_color="#004488",
                      command=lambda: messagebox.showinfo("Auto", "Генерация по выделенному тексту")) \
            .pack(side="right", padx=(12, 0))

        ctk.CTkButton(btn_container, text="Auto-Generate  Alt+Shift+Z", text_color="black", fg_color="white", width=180, height=36,
                      corner_radius=8,border_width=2, border_color="gray", command=self._open_create_window) \
            .pack(side="right")

        filter_frame = ctk.CTkFrame(self, fg_color="#e0e0e0", corner_radius=0, height=40)
        filter_frame.pack(fill="x")

        ctk.CTkLabel(filter_frame, text="Показать:", text_color="#333333") \
            .pack(side="left", padx = 10, pady = 30)

        self.filter_var = ctk.StringVar(value="Ближайшие")
        ctk.CTkComboBox(filter_frame, values=["Ближайшие", "На день", "На неделю"],
                        variable = self.filter_var, width = 140, height = 32,
                        fg_color = "#f5f5f5", border_color = "#cccccc") \
            .pack(side="left")

        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        self._render_meetings()

    def _render_meetings(self):
        for w in self.scroll_frame.winfo_children():
            w.destroy()

        for m in self.meetings:
            card = ctk.CTkFrame(self.scroll_frame, corner_radius=10, fg_color="#f8f8f8", border_width=1, border_color="#e0e0e0")
            card.pack(fill="x", pady=6, padx=2)

            top = ctk.CTkFrame(card, fg_color="transparent")
            top.pack(fill="x", padx=16, pady=(12, 6))

            ctk.CTkLabel(top, text=m.title, font=ctk.CTkFont(size=15, weight="normal"), anchor="w") \
                .pack(side="left")

            right = ctk.CTkFrame(top, fg_color="transparent")
            right.pack(side="right")

            ctk.CTkLabel(right, text="📅", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 4))
            ctk.CTkLabel(right, text=m.date, text_color="#555555", font=ctk.CTkFont(size=13)) \
                .pack(side="left", padx=(0, 12))

            ctk.CTkLabel(right, text="🕒", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 4))
            ctk.CTkLabel(right, text=m.time, text_color="#555555", font=ctk.CTkFont(size=13)) \
                .pack(side="left", padx=(0, 12))

            star_btn = ctk.CTkButton(right, text="☆", width=32, height=32, corner_radius=16,
                                     fg_color="transparent", hover_color="#e0f0ff",
                                     text_color="#888888" if not m.is_important else "#ffcc00",
                                     command=lambda: messagebox.showinfo("Star", "Переключение важности"))
            star_btn.pack(side="right")

            ctk.CTkFrame(card, height=4, fg_color="transparent").pack(fill="x", pady=(0, 8))

    def _open_create_window(self):
        MeetingWindow(self, on_create=self._on_meeting_created)

    def _on_meeting_created(self, meeting: Meeting):
        self.meetings.append(meeting)
        self._render_meetings()
        messagebox.showinfo("Создано", f"Встреча «{meeting.title}» добавлена")