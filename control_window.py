import tkinter as tk
from tkinter import font
import subprocess
from tkmacosx import Button # <-- 1. IMPORT the new Button

class CommandApp:
    def __init__(self, master):
        self.master = master
        master.title("Process Controller")
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        window_width = 300
        window_height = 175
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.master.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    def create_widgets(self):
        main_frame = tk.Frame(self.master, padx=20, pady=20)
        main_frame.pack(expand=True)

        button_font = font.Font(family='Helvetica', size=12, weight='bold')

        # 2. USE the new Button class (from tkmacosx) instead of tk.Button
        start_button = Button(
            main_frame,
            text="▶ Start",
            font=button_font,
            bg="#4CAF50",
            fg="white",
            command=self.start_command,
            width=120, # Note: tkmacosx uses pixels for width/height
            height=40
        )
        start_button.pack(pady=5)

        # USE the new Button class here as well
        end_button = Button(
            main_frame,
            text="■ End",
            font=button_font,
            bg="#f44336",
            fg="white",
            command=self.end_command,
            width=120,
            height=40
        )
        end_button.pack(pady=5)

    def _run_command(self, command, command_name):
        try:
            # result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            # print(f"{command_name} Command Output:")
            # print(result.stdout)
            # start the command but do not wait for it to finish
            subprocess.Popen(command, shell=True)
            print(f"{command_name} command started successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running {command_name.lower()} command: {e}\n{e.stderr}")

    def start_command(self):
        command = 'bash run_all.sh'
        self._run_command(command, "Start")

    def end_command(self):
        command = 'bash stop_all.sh'
        self._run_command(command, "End")

if __name__ == "__main__":
    root = tk.Tk()
    app = CommandApp(root)
    root.mainloop()