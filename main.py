import sys
from pathlib import Path
import subprocess
import time
from tkinter import TclError
from typing import Literal
import customtkinter as ctk


class Colors:
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"

    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    RESET = "\033[0m"


class WrongOption(Exception):
    """
    Wrong option chosen
    """
    pass

def push_to_textbox(text, textbox):
    textbox.configure(state="normal")
    textbox.insert("end", text + "\n")
    textbox.see("end")
    textbox.configure(state="disabled")

def debug_print(text, textbox):
    out = Colors.GREEN + Colors.BOLD + "[DEBUG]: " + Colors.RESET + text
    push_to_textbox("[DEBUG]: " + text, textbox)
    print(out)

def warning_print(text, textbox):
    out = Colors.YELLOW + Colors.BOLD  + "[WARNING]: " + Colors.RESET + text
    push_to_textbox("[WARNING]: " + text, textbox)
    print(out)

def error_print(text, textbox):
    out = Colors.RED + Colors.BOLD  + "[ERROR]: " + Colors.RESET + Colors.UNDERLINE + text + Colors.RESET
    push_to_textbox("[WARNING]: " + text, textbox)
    print(out)


class OperateApps:
    def __init__(self, textbox):
        self.out = textbox
        self.BASE_PATH = None
        if getattr(sys, 'frozen', False):
            self.BASE_PATH = Path(sys._MEIPASS)
        else:
            self.BASE_PATH = Path(__file__).parent

        self.app_exe = self.BASE_PATH / "app.exe"
        self.front_folder = self.BASE_PATH / "front"

        self.app_proc = None
        self.flask_proc = None

    def start_apps(self):
        debug_print("Starting all...", self.out)
        debug_print("Starting App Tracker...", self.out)
        self.app_proc = subprocess.Popen([str(self.app_exe)])
        debug_print("App Tracker started!", self.out)
        debug_print("Starting flask...", self.out)
        self.flask_proc = subprocess.Popen(["python", str(self.front_folder / "main.py")])
        debug_print("Flask started!", self.out)
        debug_print("All started!", self.out)

    def start_app(self, which: Literal['flask', 'tracker']):
        debug_print(f"Starting {which.title()}...", self.out)
        if which == 'tracker':
            self.app_proc = subprocess.Popen([str(self.app_exe)])
        elif which == 'flask':
            self.flask_proc = subprocess.Popen(["python", str(self.front_folder / "main.py")])
        else:
            raise WrongOption("Wrong option! Only 'flask' or 'tracker'!")

        debug_print(f"{which.title()} started!", self.out)

    def kill_app(self, which: Literal['flask', 'tracker']):
        debug_print(f"Stopping {which.title()}...", self.out)
        if which == "flask":
            if self.flask_proc and self.flask_proc.poll() is None:
                self.flask_proc.terminate()
                try:
                    self.flask_proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.flask_proc.kill()
                self.flask_proc = None
            else:
                warning_print("Cannot shut down not started procces!", self.out)
        elif which == "tracker":
            if self.app_proc and self.app_proc.poll() is None:
                self.app_proc.terminate()
                try:
                    self.app_proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.app_proc.kill()
                self.app_proc = None
            else:
                warning_print("Cannot shut down not started procces!", self.out)
        else:
            raise WrongOption("Wrong option! Only 'flask' or 'tracker'!")
        debug_print(f"{which.title()} stopped!", self.out)

    def kill_all_apps(self):
        try:
            debug_print("Stopping all...", self.out)
            for name in ("app_proc", "flask_proc"):
                debug_print(f"Stopping {name}...", self.out)
                proc = getattr(self, name)
                if proc and proc.poll() is None:
                    proc.terminate()
                    try:
                        proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        proc.kill()
                    setattr(self, name, None)
                debug_print(f"{name} stopped!", self.out)
            debug_print("All stoped!", self.out)
        except TclError:
            print("Stopping all...")
            for name in ("app_proc", "flask_proc"):
                print(f"Stopping {name}...")
                proc = getattr(self, name)
                if proc and proc.poll() is None:
                    proc.terminate()
                    try:
                        proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        proc.kill()
                    setattr(self, name, None)
                print(f"{name} stopped!")
            print("All stoped!")


class Window(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LeTime")

        self._HEIGHT = 300
        self._WIDTH = 500
        self.geometry(f"{self._WIDTH}x{self._HEIGHT}")

        self.label = ctk.CTkLabel(self, text="LeTime")
        self.label.pack()

        self.textbox = ctk.CTkTextbox(
            self,
            width=self._WIDTH,
            height=150,
        )
        self.textbox.configure(state="disabled")
        self.textbox.pack(side="top")

        self.operate_apps = OperateApps(self.textbox)

        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.pack(side="bottom", pady=10)

        if self.operate_apps.app_proc is not None:
            self.tracker_button = ctk.CTkButton(
                self.bottom_frame,
                text="Kill App Tracker",
                command=self.kill_app_proc
            )
        else:
            self.tracker_button = ctk.CTkButton(
                self.bottom_frame,
                text="Start App Tracker",
                command=self.start_app_proc
            )

        if self.operate_apps.flask_proc is not None:
            self.flask_button = ctk.CTkButton(
                self.bottom_frame,
                text="Kill Flask Server",
                command=self.kill_flask_proc
            )
        else:
            self.flask_button = ctk.CTkButton(
                self.bottom_frame,
                text="Start Flask Server",
                command=self.start_flask_proc
            )


        if self.operate_apps.flask_proc is not None or self.operate_apps.app_proc is not None:
            self.start_stop_all = ctk.CTkButton(
                self.bottom_frame,
                text="Kill all",
                command=self.operate_apps.kill_all_apps
            )
        else:
            self.start_stop_all = ctk.CTkButton(
                self.bottom_frame,
                text="Start all",
                command=self.operate_apps.start_apps
            )


        if self.tracker_button is not None:
            self.tracker_button.pack()
        else:
            error_print("Something went wrong! App Tracker button is not working properly!", self.textbox)


        if self.flask_button is not None:
            self.flask_button.pack()
        else:
            error_print("Something went wrong! Flask button is not working properly!", self.textbox)

        if self.start_stop_all is not None:
            self.start_stop_all.pack()
        self.update_buttons()

    def update_buttons(self):
        # App Tracker
        if self.operate_apps.app_proc is not None and self.operate_apps.app_proc.poll() is None:
            self.tracker_button.configure(text="Kill App Tracker", command=self.kill_app_proc)
        else:
            self.tracker_button.configure(text="Start App Tracker", command=self.start_app_proc)
        # Flask
        if self.operate_apps.flask_proc is not None and self.operate_apps.flask_proc.poll() is None:
            self.flask_button.configure(text="Kill Flask Server", command=self.kill_flask_proc)
        else:
            self.flask_button.configure(text="Start Flask Server", command=self.start_flask_proc)

        # All
        if self.operate_apps.flask_proc is not None and self.operate_apps.flask_proc.poll() is None or self.operate_apps.app_proc is not None and self.operate_apps.app_proc.poll() is None:
            self.start_stop_all.configure(text="Kill all", command=self.operate_apps.kill_all_apps)
        else:
            self.start_stop_all.configure(text="Start all", command=self.operate_apps.start_apps)

        self.after(500, self.update_buttons)

    def start_app_proc(self):
        if self.operate_apps.app_proc is None:
            self.operate_apps.start_app('tracker')
        else:
            error_print("Couldn't start App Tracker!", self.textbox)

    def start_flask_proc(self):
        if self.operate_apps.flask_proc is None:
            self.operate_apps.start_app('flask')
        else:
            error_print("Couldn't start flask!", self.textbox)

    def kill_app_proc(self):
        if self.operate_apps.app_proc is not None:
            self.operate_apps.kill_app('tracker')
        else:
            error_print("Couldn't stop App Tracker!", self.textbox)

    def kill_flask_proc(self):
        if self.operate_apps.flask_proc is not None:
            self.operate_apps.kill_app('flask')
        else:
            error_print("Couldn't stop flask!", self.textbox)


if __name__ == "__main__":
    app = Window()
    app.mainloop()

    app.operate_apps.kill_all_apps()

time.sleep(1.5) # Wait for all processes to stop

    # TODO:
    # - Edit "main.cpp" <- read_logs/database
