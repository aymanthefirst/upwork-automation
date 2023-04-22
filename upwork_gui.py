import tkinter as tk
from tkinter import messagebox
import threading
import upwork_automation_script
import sys
import io

class UpworkAutomationGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Upwork Automation")

        # Add some labels to provide context
        self.start_label = tk.Label(self.master, text="Please login to upwork and navigate and create a search for jobs. Then click start to begin the automation.")
        self.start_label.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        self.start_button = tk.Button(self.master, text="Start", command=self.start_automation, padx=10, pady=5, bg="#007bff", fg="white")
        self.start_button.grid(row=1, column=0, padx=(20, 10), pady=(0, 20))

        self.automation_thread = None
        self.stop_flag = False
        self.pause_flag = False

        # Add a Text widget to display console logs
        self.console_log = tk.Text(self.master, wrap=tk.WORD, height=10)
        self.console_log.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Redirect standard output to the Text widget
        sys.stdout = TextRedirector(self.console_log)

        def toggle_prompt_on_close():
            upwork_automation_script.prompt_on_close = not upwork_automation_script.prompt_on_close
            if upwork_automation_script.prompt_on_close:
                self.prompt_on_close_button.configure(bg="green", text="Prompt before exiting tab: ON")
            else:
                self.prompt_on_close_button.configure(bg="red", text="Prompt before exiting tab: OFF")

        self.prompt_on_close_button = tk.Button(self.master, text="Prompt before exiting tab: OFF", command=toggle_prompt_on_close)
        self.prompt_on_close_button.configure(bg="red")
        self.prompt_on_close_button.grid(row=1, column=1, padx=(10, 20), pady=(0, 20))

    def start_automation(self):
        if not self.automation_thread or not self.automation_thread.is_alive():
            self.start_label.grid_remove()
            self.stop_flag = False
            self.pause_flag = False
            self.automation_thread = threading.Thread(target=upwork_automation_script.run_automation, args=(lambda: self.stop_flag, lambda: self.pause_flag))
            self.automation_thread.start()

class TextRedirector(io.TextIOBase):
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.config(state=tk.NORMAL)
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)
        self.widget.config(state=tk.DISABLED)

    def flush(self):
        pass

def main():
    root = tk.Tk()
    gui = UpworkAutomationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
