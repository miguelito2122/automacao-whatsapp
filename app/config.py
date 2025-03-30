"""
Módulo que contém as configurações do programa.
"""
import tkinter as tk

class ToolTip:
    def __init__(self, widget, text):
        """
        Initializes a ToolTip instance with a given widget and text.

        Args:
            widget: The widget to which the tooltip will be attached.
            text: The text to display in the tooltip.

        Binds the mouse events for showing and hiding the tooltip to the widget.
        """

        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.id = None

        widget.bind("<Enter>", self.on_enter)
        widget.bind("<Leave>", self.on_leave)
        widget.bind("<Motion>", self.on_motion)

    def on_enter(self, event=None):
        """
        Shows the tooltip when the mouse enters the widget.

        Args:
            event (tkinter.Event): The event that triggered this method.
        """
        self.schedule(event)

    def on_motion(self, event):
        """
        Updates the position of the tooltip as the mouse moves over the widget.

        Args:
            event (tkinter.Event): The event containing the current mouse position.
        """

        if self.tipwindow:
            x = event.x_root + 10
            y = event.y_root + 10
            self.tipwindow.wm_geometry(f"+{x}+{y}")

    def on_leave(self, event=None):
        """
        Hides the tooltip when the mouse leaves the widget.

        Args:
            event (tkinter.Event): The event that triggered this method (optional).
        """
        self.unschedule()
        self.hide_tip()

    def schedule(self, event=None):
        """
        Schedules the tooltip to be shown after a short delay.

        Args:
            event (tkinter.Event): The event that triggered this method (optional).

        If the tooltip is already scheduled to be shown, this method will
        cancel the previous schedule and schedule a new one.
        """
        self.unschedule()
        self.id = self.widget.after(500, lambda: self.show_tip(event.x_root, event.y_root))

    def unschedule(self):
        """
        Cancels the tooltip to be shown if it is currently scheduled to be shown.

        If the tooltip is already shown, this method will not hide it.
        """
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def show_tip(self, x, y):
        """
        Shows the tooltip at the specified coordinates.

        Args:
            x (int): The x-coordinate.
            y (int): The y-coordinate.

        If the tooltip is already shown, this method will not do anything.
        """
        if self.tipwindow or not self.text:
            return
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # Remove a barra de título e bordas
        tw.wm_geometry(f"+{x + 10}+{y + 10}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self):
        """
        Hides the tooltip if it is currently shown.

        Destroys the tooltip window and sets the instance variable
        `tipwindow` to None.
        """
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

