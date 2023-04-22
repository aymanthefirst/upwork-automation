import tkinter as tk
from tkinter import messagebox
import threading
import upwork_automation_script

class UpworkAutomationGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Upwork Automation")

        # Add some labels to provide context
        self.start_label = tk.Label(self.master, text="Please login to upwork and navigate and create a search for jobs. Then click start to begin the automation.")
        self.start_label.grid(row=0, column=0, columnspan=2)

        self.start_button = tk.Button(self.master, text="Start", command=self.start_automation, padx=10, pady=5, bg="#007bff", fg="white")
        self.start_button.grid(row=1, column=0)

        self.stop_button = tk.Button(self.master, text="Stop", state=tk.DISABLED, command=self.stop_automation, padx=10, pady=5, bg="#dc3545", fg="white")
        self.stop_button.grid(row=1, column=1)

        self.exit_button = tk.Button(self.master, text="Exit", command=self.master.quit, padx=10, pady=5, bg="#6c757d", fg="white")
        self.exit_button.grid(row=2, column=0, columnspan=2)

        self.automation_thread = None
        self.stop_flag = False

    def start_automation(self):
        if not self.automation_thread or not self.automation_thread.is_alive():
            self.stop_flag = False
            self.automation_thread = threading.Thread(target=upwork_automation_script.run_automation, args=(lambda: self.stop_flag,))
            self.automation_thread.start()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

    def stop_automation(self):
        self.stop_flag = True
        self.automation_thread.join()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    gui = UpworkAutomationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
