from idlelib.tooltip import Hovertip

import customtkinter as ctk
from tkinter import messagebox
from data.entities.meeting import Meeting
from ui.view_models.main_window_view_model import MainWindowViewModel
from ui.views.loader import CircularLoader
from ui.views.meeting_window import MeetingWindow


class MainWindow(ctk.CTkToplevel):
    def __init__(self, root, repository, on_auto_generate=None, on_close=None):
        super().__init__(root)
        self.title("Meeting Planner")
        self.geometry("860x620")
        self.minsize(720, 500)

        # Double buffering
        self.form = ctk.CTkFrame(self, fg_color="transparent")
        self.buffer = ctk.CTkFrame(self, fg_color="transparent")
        self.form.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)
        self.buffer.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)
        self.buffer.lower(self.form)

        self.view_model = MainWindowViewModel(repository)
        self.loaders = []

        self.on_auto_generate = lambda: print("Auto-generate clicked - use Alt+Shift+Z") if on_auto_generate is None else on_auto_generate
        self.on_close = lambda: self.destroy() if on_close is None else on_close
        self.protocol("WM_DELETE_WINDOW", on_close)

        self.view_model.get_meetings()
        self.meetings = self.view_model.meetings

        self._build_ui()

    def _start_load(self, loader: CircularLoader, loader_x, loader_y):
        self.view_model.loading = True
        self.loader = loader
        loader.place(relx=loader_x, rely=loader_y, anchor="center")
        self.config(cursor="watch")

    def _end_load(self):
        self.view_model.loading = False
        self.view_model.loader_angle = self.loader.angle
        self.config(cursor="")

    def _build_ui(self):
        self._start_load(CircularLoader(self.form, size=50, color="#1e90ff", bgcolor="#eeeeee",
                                        angle=self.view_model.loader_angle),
                         0.5, 0.5)
        for child in self.buffer.winfo_children():
            child.destroy()

        top_frame = ctk.CTkFrame(self.buffer, fg_color="white", corner_radius=0, height=56)
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
                      text_color="white", command=self._open_meeting_window) \
            .pack(side="left")

        self.main_frame = ctk.CTkFrame(self.buffer, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)
        self.meetings_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.meetings_buffer = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.meetings_frame.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)
        self.meetings_buffer.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)
        self.meetings_buffer.lower(self.meetings_frame)

        self.filter_var = ctk.StringVar(value="Ближайшие")
        self._on_filter_change("Ближайшие")

        def finish_render():
            if not self.view_model.loading:
                self.form, self.buffer = (self.buffer, self.form)
                self.update_idletasks()
                self._end_load()
                self.form.tkraise(self.buffer)
            else:
                self.after(50, lambda: finish_render())

        finish_render()

    def _build_filter_frame(self):
        filter_frame = ctk.CTkFrame(self.meetings_buffer, fg_color="#e0e0e0", corner_radius=0, height=40)
        filter_frame.pack(fill="x")

        ctk.CTkLabel(filter_frame, text="Показать:", text_color="#333333") \
            .pack(side="left", padx=10, pady=30)

        self.filter_combo = ctk.CTkComboBox(filter_frame,
                                            values=["Ближайшие", "На день", "На неделю", "Важные", "Все"],
                                            variable=self.filter_var, width=140, height=32,
                                            fg_color="#f5f5f5", border_color="#cccccc",
                                            command=self._on_filter_change,
                                            state="readonly")
        self.filter_combo.pack(side="left")

        right_part = ctk.CTkFrame(filter_frame, fg_color="transparent")
        right_part.pack(side="right", padx=20, pady=8)

        self.count_label = ctk.CTkLabel(right_part, text=f"",
                                        text_color="#555555", font=ctk.CTkFont(size=14))
        self.count_label.pack(side="right")

    def _on_auto_generate(self):
        if self.on_auto_generate:
            self.on_auto_generate()

    def _open_meeting_window(self, meeting=None):
        MeetingWindow(self,
                      repository=self.view_model.repository,
                      on_save=self.on_meeting_saved if meeting is None else self._on_meeting_edit,
                      prefill_meeting=meeting)

    def _on_meeting_edit(self, meeting: Meeting):
        self.on_meeting_saved(meeting, creating=False)

    def on_meeting_saved(self, meeting: Meeting, creating=True):
        self._start_load(
            CircularLoader(self.meetings_frame, size=30, color="#1e90ff", bgcolor="#e0e0e0",
                           angle=self.view_model.loader_angle),
            0.3, 0.08
        )
        if self.view_model.add_meeting(meeting):
            self._render_meetings()
        if creating:
            messagebox.showinfo("Создано", f"Встреча «{meeting.title}» добавлена")
        else:
            messagebox.showinfo("Успешно", f"Встреча «{meeting.title}» изменена")
        self._end_load()

    def _on_filter_change(self, choice):
        if choice == self.view_model.filter:
            return

        self._start_load(
            CircularLoader(self.meetings_frame, size=30, color="#1e90ff", bgcolor="#e0e0e0",
                           angle=self.view_model.loader_angle),
            0.3, 0.08
        )
        self.view_model.filter_meetings(choice)
        self._render_meetings()

    def _render_meetings(self):
        for child in self.meetings_buffer.winfo_children():
            child.destroy()

        self._build_filter_frame()
        self.scroll_frame = ctk.CTkScrollableFrame(self.meetings_buffer, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        filtered_meetings = self.view_model.display_meetings

        def update_frame():
            self.meetings_frame, self.meetings_buffer = (self.meetings_buffer, self.meetings_frame)
            self.update_idletasks()
            self._end_load()
            self.meetings_frame.tkraise(self.meetings_buffer)

        if self.view_model.error_display:
            self.count_label.configure(text=f"")
            empty_label = ctk.CTkLabel(
                self.scroll_frame,
                text=self.view_model.error_text,
                font=ctk.CTkFont(size=14),
                text_color="#EE1010"
            )
            empty_label.pack(expand=True, pady=50)
            update_frame()
            return

        if not filtered_meetings:
            self.count_label.configure(text=f"")
            empty_label = ctk.CTkLabel(
                self.scroll_frame,
                text="Нет встреч в выбранном периоде",
                font=ctk.CTkFont(size=14),
                text_color="#999999"
            )
            empty_label.pack(expand=True, pady=50)
            update_frame()
            return

        self.count_label.configure(text=f"{len(filtered_meetings)} встречи")

        def _build_card(index):
            if index < len(self.view_model.display_meetings):
                self._build_meeting_card(self.view_model.display_meetings[index])
                self.after(50, lambda: _build_card(index + 1))
            else:
                update_frame()

        _build_card(0)

    def _build_meeting_card(self, m):
        card = ctk.CTkFrame(self.scroll_frame, corner_radius=15, fg_color="#f8f8f8",
                            border_width=2, border_color="#e0e0e0")
        card.pack(fill="x", pady=6, padx=2)

        top = ctk.CTkFrame(card, fg_color="transparent")
        top.pack(fill="x", padx=16, pady=(12, 6))

        ctk.CTkLabel(top, text=m.title, font=ctk.CTkFont(size=15, weight="normal"), anchor="w") \
            .pack(side="left", fill="x", expand=True)

        right_frame = ctk.CTkFrame(top, fg_color="transparent")
        right_frame.pack(side="right")

        datetime_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        datetime_frame.pack(side="left")

        (ctk.CTkLabel(datetime_frame, text="📅", font=ctk.CTkFont(size=14))
         .pack(side="left", padx=(0, 4), pady=(0, 4)))
        date_label = ctk.CTkLabel(datetime_frame, text=m.date, text_color="#555555", font=ctk.CTkFont(size=13))
        date_label.pack(side="left", padx=(0, 12))
        Hovertip(date_label, "Дата встречи", hover_delay=300)

        (ctk.CTkLabel(datetime_frame, text="🕒", font=ctk.CTkFont(size=14))
         .pack(side="left", padx=(0, 4), pady=(0, 4)))
        time_label = ctk.CTkLabel(datetime_frame, text=m.time, text_color="#555555", font=ctk.CTkFont(size=13))
        time_label.pack(side="left", padx=(0, 12))
        Hovertip(time_label, "Время встречи", hover_delay=300)

        actions_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        actions_frame.pack(side="left", padx=(16, 0))

        star_btn = ctk.CTkButton(
            actions_frame, text="★" if m.is_important else "☆",
            width=28, height=28, corner_radius=14,
            fg_color="transparent", hover_color="#e0f0ff",
            text_color="#ffcc00" if m.is_important else "#888888",
            command=None,
            anchor="center"
        )
        hovertip = Hovertip(star_btn, "Снять отметку" if m.is_important else "Отметить важной", hover_delay=300)
        star_btn.configure(command=lambda meeting=m: self._toggle_importance(meeting, star_btn, hovertip))
        star_btn.pack(side="left", padx=1)

        edit_btn = ctk.CTkButton(
            actions_frame, text="✏", width=28, height=28, corner_radius=14,
            fg_color="transparent", hover_color="#e0f0ff",
            text_color="#888888",
            command=lambda meeting=m: self._open_meeting_window(meeting),
            anchor="center"
        )
        Hovertip(edit_btn, "Редактировать встречу", hover_delay=300)
        edit_btn.pack(side="left", padx=1)

        delete_btn = ctk.CTkButton(
            actions_frame, text="X", width=28, height=28, corner_radius=14,
            fg_color="transparent", hover_color="#ffe5e5",
            text_color="#888888",
            command=lambda meeting=m: self._delete_meeting(meeting),
            anchor="center"
        )
        Hovertip(delete_btn, "Отменить встречу", hover_delay=300)
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

    def _toggle_importance(self, meeting, btn, hovertip: Hovertip):
        if self.view_model.toggle_importance(meeting):
            btn.configure(text="★" if meeting.is_important else "☆",
                          text_color="#ffcc00" if meeting.is_important else "#888888")
            hovertip.text = "Снять отметку" if meeting.is_important else "Отметить важной"
        else:
            messagebox.showwarning("Ошибка", "Не удалось изменить статус встречи.")

    def _delete_meeting(self, meeting):
        if messagebox.askyesno("Удаление", f"Удалить встречу «{meeting.title}»?"):
            self._start_load(
                CircularLoader(self.meetings_frame, size=30, color="#1e90ff", bgcolor="#e0e0e0",
                               angle=self.view_model.loader_angle),
                0.3, 0.08
            )
            if self.view_model.delete_meeting(meeting):
                self._render_meetings()
            else:
                messagebox.showwarning("Ошибка", "Ошибка при удалении встречи.")
                self._end_load()
