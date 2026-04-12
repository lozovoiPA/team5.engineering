import customtkinter as ctk


class CircularLoader(ctk.CTkCanvas):
    def __init__(self, master, size=50, color="blue", bgcolor="#eeeeee", angle=0):
        super().__init__(master, width=size, height=size, highlightthickness=0, bg=bgcolor)
        self.angle = angle
        self.arc = self.create_arc(5, 5, size-5, size-5, start=0, extent=120, outline=color, style="arc", width=4)

        self.animating = True
        self.animate()

    def animate(self):
        self.angle = (self.angle + 20) % 360
        self.itemconfig(self.arc, start=self.angle)
        if self.animating:
            self.after(30, lambda: self.animate())
