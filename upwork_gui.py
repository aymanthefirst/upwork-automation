import tkinter as tk
from tkinter import messagebox
import threading
import upwork_automation_script
import sys
import io
import tkinter

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

        self.skip_matching = False

        # Add a Text widget to display console logs
        self.console_log = tk.Text(self.master, wrap=tk.WORD, height=10)
        self.console_log.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Redirect standard output to the Text widget
        sys.stdout = TextRedirector(self.console_log)

        def toggle_skip_matching():
            self.skip_matching = not self.skip_matching
            print(f"Skip matching: {self.skip_matching}")
            if self.skip_matching:
                skip_matching_button.configure(bg="green", text="Skip Matching: ON")
            else:
                skip_matching_button.configure(bg="red", text="Skip Matching: OFF")
        
        def toggle_prompt_on_close():
            upwork_automation_script.prompt_on_close = not upwork_automation_script.prompt_on_close
            if upwork_automation_script.prompt_on_close:
                self.prompt_on_close_button.configure(bg="green", text="Prompt before exiting tab: ON")
            else:
                self.prompt_on_close_button.configure(bg="red", text="Prompt before exiting tab: OFF")

        self.prompt_on_close_button = tk.Button(self.master, text="Prompt before exiting tab: OFF", command=toggle_prompt_on_close)
        self.prompt_on_close_button.configure(bg="red")
        self.prompt_on_close_button.grid(row=1, column=1, padx=(10, 20), pady=(0, 20))

        skip_matching_button = tkinter.Button(text="Skip Matching: OFF", command=toggle_skip_matching, bg="red")
        skip_matching_button.grid(row=3, column=0, columnspan=2, pady=(0, 20))

        skip_matching_button = tkinter.Button(text="Skip Matching: OFF", command=toggle_skip_matching, bg="red")
        skip_matching_button.grid(row=3, column=0, columnspan=2, pady=(0, 20))

        self.keywords_label = tk.Label(self.master, text="Please enter the keywords to avoid:")
        self.keywords_label.grid(row=4, column=0, padx=(20, 10), pady=(0, 5), sticky='w')

        self.keywords_entry = tk.Entry(self.master, width=60)
        self.keywords_entry.grid(row=4, column=1, padx=(0, 10), pady=(0, 20), sticky='w')

        def save_keywords():
            keywords = self.keywords_entry.get()
            # Save the keywords or perform the desired action
            print("Keywords saved:", keywords)

        self.save_button = tk.Button(self.master, text="Save", command=save_keywords, padx=10, pady=5, bg="#007bff", fg="white")
        self.save_button.grid(row=4, column=2, padx=(0, 20), pady=(0, 20), sticky='w')


    def start_automation(self):
        if not self.automation_thread or not self.automation_thread.is_alive():
            self.start_label.grid_remove()
            self.stop_flag = False
            self.pause_flag = False
            self.automation_thread = threading.Thread(target=upwork_automation_script.run_automation, args=(lambda: self.stop_flag, lambda: self.pause_flag, self))
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
