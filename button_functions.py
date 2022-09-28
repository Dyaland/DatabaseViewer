import tkinter as tk


class ButtonFunctions:
    """Class used by the button classes and imported by main file"""
    def __init__(self):
        # Button states
        self.selected = {"bg": "light green", "relief": "sunken"}
        self.unselected = {"bg": "light gray", "relief": "raised"}

    def on_enter(self, _):
        if _.widget["relief"] != tk.SUNKEN:
            _.widget.config(bg="#e8e8e8")  # Lighter gray

    def on_leave(self, _):
        if _.widget["relief"] != tk.SUNKEN:
            _.widget.config(bg="light gray")

    def click_down(self, _):
        _.widget.config(relief=tk.SUNKEN)

    def click_release(self, _):
        _.widget.config(relief=tk.RAISED)

    def disable(self, button):
        button.unbind("<Button-1>")
        button.unbind("<Enter>")
        button["state"] = "disabled"

    def enable(self, button):
        button.bind("<Enter>", self.on_enter)
        button["state"] = "normal"


class MyButton(ButtonFunctions):
    """Class for general buttons"""
    def __init__(self, frame, name):
        super().__init__()

        self.button = tk.Label(frame, text=name, width=12, bd=2, relief="raised")
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)

    def create(self):
        return self.button


class DisabledButton(MyButton):
    """Class for initially disabled buttons"""
    def __init__(self, frame, name):
        super().__init__(frame, name)
        self.disable(self.button)


class PressReleaseButton(MyButton):
    """Class for buttons with on-click effect"""
    def __init__(self, frame, name):
        super().__init__(frame, name)
        self.button.bind("<ButtonPress-1>", self.click_down)
        self.button.bind("<ButtonRelease-1>", self.click_release)


class OkButton(MyButton):
    def __init__(self, frame, name):
        super().__init__(frame, name)
        self.button.config(width=6)
        self.disable(self.button)


class ExecuteButton(MyButton):
    def __init__(self, frame, name):
        super().__init__(frame, name)
        self.button.config(width=14)
        self.disable(self.button)
