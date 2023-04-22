import tkinter as tk
from tkinter import messagebox
import threading
import upwork_automation_script
import sys
import io

def toggle_prompt_on_close():
    upwork_automation_script.prompt_on_close = not upwork_automation_script.prompt_on_close
    prompt_on_close_button.config(text=f"Prompt on Close: {upwork_automation_script.prompt_on_close}")

root = tk.Tk()
root.title("Upwork Automation")

class UpworkAutomationGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Upwork import tkinter as tk
from tkinter import ttk
import upwork_automation_script

def toggle_prompt_on_close():
    upwork_automation_script.prompt_on_close = not upwork_automation_script.prompt_on_close
    prompt_on_close_button.config(text=f"Prompt on Close: {upwork_automation_script.prompt_on_close}")

root = tk.Tk()
root.title("Upwork Automation")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Add input fields, labels, and buttons as needed
# For example:
username_label = ttk.Label(mainframe, text="Username:")
username_label.grid(column=1, row=1, sticky=tk.W)
username_entry = ttk.Entry(mainframe)
username_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))

password_label = ttk.Label(mainframe, text="Password:")
password_label.grid(column=1, row=2, sticky=tk.W)
password_entry = ttk.Entry(mainframe, show="*")
password_entry.grid(column=2, row=2, sticky=(tk.W, tk.E))

submit_button = ttk.Button(mainframe, text="Submit", command=upwork_automation_script.some_function)  # Replace "some_function" with the actual function
submit_button.grid(column=2, row=3, sticky=tk.W)

# Add a button to toggle the prompt on close behavior
prompt_on_close_button = ttk.Button(mainframe, text=f"Prompt on Close: {upwork_automation_script.prompt_on_close}", command=toggle_prompt_on_close)
prompt_on_close_button.grid(column=2, row=4, sticky=tk.W)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
Automation")

        # Add some labels to provide context
        self.start_label = tk.Label(self.master, text="Please login to upwork and navigate and create a search for jobs. Then click start to begin the automation.")
        self.start_label.grid(row=0, column=0, columnspan=3)

        self.start_button = tk.Button(self.master, text="Start", command=self.start_automation, padx=10, pady=5, bg="#007bff", fg="white")
        self.start_button.grid(row=1, column=0)

        self.pause_button = tk.Button(self.master, text="Pause", state=tk.DISABLED, command=self.pause_automation, padx=10, pady=5, bg="#ffc107", fg="white")
        self.pause_button.grid(row=1, column=1)

        self.stop_button = tk.Button(self.master, text="Stop", state=tk.DISABLED, command=self.stop_automation, padx=10, pady=5, bg="#dc3545", fg="white")
        self.stop_button.grid(row=1, column=2)

        self.exit_button = tk.Button(self.master, text="Exit", command=self.master.quit, padx=10, pady=5, bg="#6c757d", fg="white")
        self.exit_button.grid(row=2, column=0, columnspan=3)

        self.automation_thread = None
        self.stop_flag = False
        self.pause_flag = False

        # Add a Text widget to display console logs
        self.console_log = tk.Text(self.master, wrap=tk.WORD, height=10)
        self.console_log.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        # Redirect standard output to the Text widget
        sys.stdout = TextRedirector(self.console_log)

    def start_automation(self):
        if not self.automation_thread or not self.automation_thread.is_alive():
            self.start_label.grid_remove()
            self.stop_flag = False
            self.pause_flag = False
            self.automation_thread = threading.Thread(target=upwork_automation_script.run_automation, args=(lambda: self.stop_flag, lambda: self.pause_flag))
            self.automation_thread.start()
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)


    def pause_automation(self):
        self.pause_flag = not self.pause_flag
        if self.pause_flag:
            self.pause_button.config(text="Resume")
        else:
            self.pause_button.config(text="Pause")

    def stop_automation(self):
        self.stop_flag = True
        self.automation_thread.join()
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)

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
