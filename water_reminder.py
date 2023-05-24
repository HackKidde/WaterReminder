import tkinter as tk
from tkinter import messagebox
from pystray import MenuItem as tray_menu_item
import pystray
from PIL import Image
import threading
import time
from win10toast import ToastNotifier
import sys

class ReminderApp:
    def __init__(self):
        self.interval = 0
        self.timer_thread = None
        self.root = tk.Tk()
        self.root.title("Water Reminder App")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.interval_label = tk.Label(self.root, text="Set Reminder Interval (mins):", font=("Arial", 16))
        self.interval_label.pack()

        self.interval_entry = tk.Entry(self.root, font=("Arial", 16))
        self.interval_entry.pack()

        self.button = tk.Button(self.root, text="Set Reminder", font=("Arial", 16), command=self.start_reminder)
        self.button.pack(pady=10)

        self.icon = None
        self.create_system_tray()

    def start_reminder(self):
        if self.timer_thread and self.timer_thread.is_alive():
            messagebox.showwarning("Reminder In Progress", "A reminder is already set.")
        else:
            interval = self.interval_entry.get()
            try:
                self.interval = int(interval)
                if self.interval > 0:
                    self.timer_thread = threading.Thread(target=self.timer_loop)
                    self.timer_thread.start()
                    self.root.iconify()  # Minimize the window after setting the reminder
                else:
                    messagebox.showerror("Invalid Interval", "Please enter a positive interval")
            except ValueError:
                messagebox.showerror("Invalid Interval", "Please enter a valid interval")

    def timer_loop(self):
        try:
            while True:
                time.sleep(self.interval * 60)
                self.show_reminder()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_reminder(self):
        try:
            toaster = ToastNotifier()
            toaster.show_toast(
                "Reminder",
                "Time to drink water!",
                icon_path="icon.ico",
                duration=10,
                threaded=True
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_close(self):
        try:
            self.root.iconify()  # Minimize the window before destroying it
            if self.timer_thread and self.timer_thread.is_alive():
                self.timer_thread.join()
            if self.icon:
                self.icon.stop()  # Stop the system tray icon
            self.root.destroy()
            sys.exit(0)  # Terminate the application process
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def change_interval(self):
        try:
            self.root.iconify()  # Minimize the window before creating a new instance
            if self.icon:
                self.icon.stop()  # Stop the system tray icon
            new_app = ReminderApp()
            new_app.run()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_system_tray(self):
        try:
            image = Image.open("icon.png")
            menu = (tray_menu_item('Change Interval', self.change_interval), tray_menu_item('Exit', self.on_close))
            self.icon = pystray.Icon("Water Reminder App", image, "Water Reminder App", menu)
            self.icon.run()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = ReminderApp()
    app.run()
