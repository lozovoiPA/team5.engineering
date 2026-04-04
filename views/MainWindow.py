import customtkinter as ctk
from tkinter import messagebox
from data.entities.meeting import Meeting
from views.MeetingWindow import MeetingWindow
from datetime import datetime


class MainWindow(ctk.CTkToplevel):
    def __init__(self, root, on_auto_generate=None):
        super().__init__(root)
        self.title("Meeting Planner")
        self.geometry("860x620")
        self.minsize(720, 500)

        self.on_auto_generate = on_auto_generate

        self.meetings = [
            Meeting("Встреча по ML", "22.04.2026", "13:35", id=1),
            Meeting("Встреча по LLM", "22.04.2026", "12:35", is_important=True, id=2),
            Meeting("Встреча 1", "22.04.2026", "11:35", id=3),
            Meeting("Встреча 2", "22.04.2026", "13:35", id=4),
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

        ctk.CTkButton(btn_container, text="Auto-Generate  Alt+Shift+Z", width=200, height=36,
                      corner_radius=8, fg_color="white", text_color="black",
                      border_width=2, border_color="gray", hover_color="#f0f0f0",
                      command=self._on_auto_generate) \
            .pack(side="left", padx=(0, 12))

        ctk.CTkButton(btn_container, text="+ Создать встречу", width=160, height=36,
                      corner_radius=8, fg_color="#0066cc", hover_color="#0055aa",
                      text_color="white", command=self._open_create_window) \
            .pack(side="left")

        filter_frame = ctk.CTkFrame(self, fg_color="#e0e0e0", corner_radius=0, height=40)
        filter_frame.pack(fill="x")

        ctk.CTkLabel(filter_frame, text="Показать:", text_color="#333333") \
            .pack(side="left", padx=10, pady=30)

        self.filter_var = ctk.StringVar(value="Ближайшие")
        self.filter_combo = ctk.CTkComboBox(filter_frame,
                                            values=["Ближайшие", "На день", "На неделю", "Важные"],
                                            variable=self.filter_var, width=140, height=32,
                                            fg_color="#f5f5f5", border_color="#cccccc",
                                            command=self._on_filter_change)
        self.filter_combo.pack(side="left")

        right_part = ctk.CTkFrame(filter_frame, fg_color="transparent")
        right_part.pack(side="right", padx=20, pady=8)

        self.count_label = ctk.CTkLabel(right_part, text=f"{len(self.meetings)} встречи",
                                        text_color="#555555", font=ctk.CTkFont(size=14))
        self.count_label.pack(side="right")

        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        self._render_meetings()

    def _on_auto_generate(self):
        if self.on_auto_generate:
            self.on_auto_generate()

    def _open_create_window(self):
        MeetingWindow(self, on_create=self._on_meeting_created)

    def _on_meeting_created(self, meeting: Meeting):
        if not meeting.id or meeting.id == 0:
            max_id = max([m.id for m in self.meetings], default=0)
            meeting.id = max_id + 1
        self.meetings.append(meeting)
        self._render_meetings()
        messagebox.showinfo("Создано", f"Встреча «{meeting.title}» добавлена")

    def _on_filter_change(self, choice):
        self._render_meetings()

    def _get_filtered_meetings(self):
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        filter_type = self.filter_var.get()

        filtered = []
        for meeting in self.meetings:
            try:
                meeting_date = datetime.strptime(meeting.date, "%d.%m.%Y")
                meeting_date = meeting_date.replace(hour=0, minute=0, second=0, microsecond=0)
                days_diff = (meeting_date - current_date).days

                if filter_type == "Ближайшие":
                    if days_diff >= 0:
                        filtered.append(meeting)
                elif filter_type == "На день":
                    if days_diff == 0:
                        filtered.append(meeting)
                elif filter_type == "На неделю":
                    if 0 <= days_diff <= 7:
                        filtered.append(meeting)
                elif filter_type == "Важные":
                    if meeting.is_important:
                        filtered.append(meeting)
            except Exception as e:
                print(f"Ошибка парсинга даты {meeting.date}: {e}")
                filtered.append(meeting)

        try:
            filtered.sort(key=lambda m: (
                datetime.strptime(m.date, "%d.%m.%Y") if m.date else datetime.max,
                m.time if m.time else "23:59"
            ))
        except:
            pass

        return filtered

    def _render_meetings(self):
        for w in self.scroll_frame.winfo_children():
            w.destroy()

        filtered_meetings = self._get_filtered_meetings()
        self.count_label.configure(text=f"{len(filtered_meetings)} встречи")

        if not filtered_meetings:
            empty_label = ctk.CTkLabel(
                self.scroll_frame,
                text="Нет встреч в выбранном периоде",
                font=ctk.CTkFont(size=14),
                text_color="#999999"
            )
            empty_label.pack(expand=True, pady=50)
            return

        for m in filtered_meetings:
            card = ctk.CTkFrame(self.scroll_frame, corner_radius=10, fg_color="#f8f8f8",
                                border_width=1, border_color="#e0e0e0")
            card.pack(fill="x", pady=6, padx=2)

            top = ctk.CTkFrame(card, fg_color="transparent")
            top.pack(fill="x", padx=16, pady=(12, 6))

            ctk.CTkLabel(top, text=m.title, font=ctk.CTkFont(size=15, weight="normal"), anchor="w") \
                .pack(side="left", fill="x", expand=True)

            right_frame = ctk.CTkFrame(top, fg_color="transparent")
            right_frame.pack(side="right")

            datetime_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
            datetime_frame.pack(side="left")

            ctk.CTkLabel(datetime_frame, text="📅", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 4))
            ctk.CTkLabel(datetime_frame, text=m.date, text_color="#555555", font=ctk.CTkFont(size=13)) \
                .pack(side="left", padx=(0, 12))

            ctk.CTkLabel(datetime_frame, text="🕒", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 4))
            ctk.CTkLabel(datetime_frame, text=m.time, text_color="#555555", font=ctk.CTkFont(size=13)) \
                .pack(side="left", padx=(0, 12))

            actions_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
            actions_frame.pack(side="left", padx=(16, 0))

            star_btn = ctk.CTkButton(
                actions_frame, text="★" if m.is_important else "☆",
                width=28, height=28, corner_radius=14,
                fg_color="transparent", hover_color="#e0f0ff",
                text_color="#ffcc00" if m.is_important else "#888888",
                command=lambda meeting=m: self._toggle_importance(meeting)
            )
            star_btn.pack(side="left", padx=1)

            edit_btn = ctk.CTkButton(
                actions_frame, text="✏", width=28, height=28, corner_radius=14,
                fg_color="transparent", hover_color="#e0f0ff",
                text_color="#888888",
                command=lambda meeting=m: self._edit_meeting(meeting)
            )
            edit_btn.pack(side="left", padx=1)

            delete_btn = ctk.CTkButton(
                actions_frame, text="🗑", width=28, height=28, corner_radius=14,
                fg_color="transparent", hover_color="#e0f0ff",
                text_color="#888888",
                command=lambda meeting=m: self._delete_meeting(meeting)
            )
            delete_btn.pack(side="left", padx=1)

            if m.description:
                desc_label = ctk.CTkLabel(
                    card,
                    text=m.description,
                    font=ctk.CTkFont(size=12),
                    text_color="#777777",
                    anchor="w",
                    wraplength=600
                )
                desc_label.pack(fill="x", padx=16, pady=(0, 8))

            ctk.CTkFrame(card, height=4, fg_color="transparent").pack(fill="x", pady=(0, 8))

    def _toggle_importance(self, meeting):
        meeting.is_important = not meeting.is_important
        self._render_meetings()
        status = "важной" if meeting.is_important else "обычной"
        messagebox.showinfo("Важность", f"Встреча «{meeting.title}» отмечена как {status}")

    def _edit_meeting(self, meeting):
        MeetingWindow(self, on_create=self._on_meeting_edited, prefill_meeting=meeting)

    def _on_meeting_edited(self, updated_meeting: Meeting):
        for i, m in enumerate(self.meetings):
            if m.id == updated_meeting.id:
                self.meetings[i] = updated_meeting
                break
        self._render_meetings()
        messagebox.showinfo("Обновлено", f"Встреча «{updated_meeting.title}» обновлена")

    def _delete_meeting(self, meeting):
        if messagebox.askyesno("Удаление", f"Удалить встречу «{meeting.title}»?"):
            self.meetings = [m for m in self.meetings if m.id != meeting.id]
            self._render_meetings()