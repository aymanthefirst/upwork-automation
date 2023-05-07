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

        self.start_label = tk.Label(self.master, text="Please login to upwork and navigate and create a search for jobs. Then click start to begin the automation.")
        self.start_label.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        self.start_button = tk.Button(self.master, text="Start", command=self.start_automation, padx=10, pady=5, bg="#007bff", fg="white")
        self.start_button.grid(row=1, column=0, padx=(20, 10), pady=(0, 20))

        self.automation_thread = None
        self.stop_flag = False
        self.pause_flag = False

        self.console_log = tk.Text(self.master, wrap=tk.WORD, height=10)
        self.console_log.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        sys.stdout = TextRedirector(self.console_log)

        self.tokens_used = tk.IntVar()
        self.tokens_used.set(0)
        self.tokens_used_label = tk.Label(self.master, text="Tokens used:")
        self.tokens_used_label.grid(
            row=5, column=0, padx=(20, 10), pady=(0, 5), sticky='w')
        self.tokens_used_value_label = tk.Label(
            self.master, textvariable=self.tokens_used)
        self.tokens_used_value_label.grid(
            row=5, column=1, padx=(0, 10), pady=(0, 20), sticky='w')
        
        self.price_label = tk.Label(self.master, text="Price:")
        self.price_label.grid(
            row=6, column=0, padx=(20, 10), pady=(0, 5), sticky='w')
        self.price = tk.StringVar()
        self.price.set("$0")
        self.price_value_label = tk.Label(
            self.master, textvariable=self.price)
        self.price_value_label.grid(
            row=6, column=1, padx=(0, 10), pady=(0, 20), sticky='w')
        
        self.number_of_submits_label = tk.Label(self.master, text="Number of submits:")
        self.number_of_submits_label.grid(
            row=7, column=0, padx=(20, 10), pady=(0, 5), sticky='w')
        self.number_of_submits = tk.IntVar()
        self.number_of_submits.set(0)
        self.number_of_submits_value_label = tk.Label(
            self.master, textvariable=self.number_of_submits)
        self.number_of_submits_value_label.grid(
            row=7, column=1, padx=(0, 10), pady=(0, 20), sticky='w')

        upwork_automation_script.prompt_on_close = True
        def toggle_prompt_on_close():
            upwork_automation_script.prompt_on_close = not upwork_automation_script.prompt_on_close
            if upwork_automation_script.prompt_on_close:
                self.prompt_on_close_button.configure(bg="green", text="Prompt before exiting tab: ON")
            else:
                self.prompt_on_close_button.configure(
                    bg="#007bff", fg="white", text="Prompt before exiting tab: OFF")
        self.prompt_on_close_button = tk.Button(self.master, text="Prompt before exiting tab: ON", command=toggle_prompt_on_close)
        self.prompt_on_close_button.configure(bg="green")
        self.prompt_on_close_button.grid(
            row=3, column=0, padx=(20, 5), pady=(0, 20))


        upwork_automation_script.submit_applications = False
        def toggle_submit_applications():
            upwork_automation_script.submit_applications = not upwork_automation_script.submit_applications
            if upwork_automation_script.submit_applications:
                self.submit_applications_button.configure(bg="green", text="Submit applications: ON")
            else:
                self.submit_applications_button.configure(
                    bg="#007bff", fg="white", text="Submit applications: OFF")
        self.submit_applications_button = tk.Button(self.master, text="Submit applications: OFF", command=toggle_submit_applications)
        self.submit_applications_button.configure(bg="#007bff", fg="white")
        self.submit_applications_button.grid(
            row=3, column=1, padx=(5, 5), pady=(0, 20))



        upwork_automation_script.auto_generate_cover_letter = False
        def toggle_auto_generate_cover_letter():
            upwork_automation_script.auto_generate_cover_letter = not upwork_automation_script.auto_generate_cover_letter
            if upwork_automation_script.auto_generate_cover_letter:
                self.auto_generate_cover_letter_button.configure(
                    bg="green", text="Auto generate cover letter: ON")
            else:
                self.auto_generate_cover_letter_button.configure(
                    bg="#007bff", fg="white", text="Auto generate cover letter: OFF")
        self.auto_generate_cover_letter_button = tk.Button(
            self.master, text="Auto generate cover letter: OFF", command=toggle_auto_generate_cover_letter)
        self.auto_generate_cover_letter_button.configure(
            bg="#007bff", fg="white")
        self.auto_generate_cover_letter_button.grid(
            row=3, column=2, padx=(5, 10), pady=(0, 20))



        

        

        self.keywords_label = tk.Label(self.master, text="Please enter the keywords to avoid:")
        self.keywords_label.grid(row=4, column=0, padx=(20, 10), pady=(0, 5), sticky='w')

        self.keywords_entry = tk.Entry(self.master, width=60)
        self.keywords_entry.insert(0, "applied")
        self.keywords_entry.grid(row=4, column=1, padx=(0, 10), pady=(0, 20), sticky='w')

        self.application_limit_label = tk.Label(
            self.master, text="Application limit:")
        self.application_limit_label.grid(
            row=5, column=0, padx=(20, 10), pady=(0, 5), sticky='w')
        self.application_limit_spinbox = tk.Spinbox(
            self.master, from_=1, to=1000, width=10)
        self.application_limit_spinbox.delete(0, 'end')
        self.application_limit_spinbox.insert(0, "10")
        self.application_limit_spinbox.grid(
            row=5, column=1, padx=(0, 10), pady=(0, 20), sticky='w')

        self.application_limit = 10
        def save_keywords_and_limit():
            keywords = self.keywords_entry.get()
            with open("keywords_to_avoid.txt", "w") as file:
                file.write(keywords)
            print("Keywords saved:", keywords)

            self.application_limit = int(self.application_limit_spinbox.get())
            print("Application limit saved:", self.application_limit)

        self.save_button = tk.Button(self.master, text="Save", command=save_keywords_and_limit, padx=10, pady=5, bg="#007bff", fg="white")
        self.save_button.grid(row=7, column=2, padx=(0, 20), pady=(0, 20), sticky='se')

    def update_tokens_used(self, count):
        self.tokens_used.set(count)
        price_per_token = 0.002 / 1000
        price = count * price_per_token
        self.price.set(f"${price:.4f}")

    def add_one_submit(self):
        self.number_of_submits.set(self.number_of_submits.get() + 1)

    def start_automation(self):
        if not self.automation_thread or not self.automation_thread.is_alive():
            self.start_label.grid_remove()
            self.stop_flag = False
            self.pause_flag = False
            self.automation_thread = threading.Thread(target=upwork_automation_script.run_automation, args=(
                upwork_automation_script.auto_generate_cover_letter, lambda: self.stop_flag, lambda: self.pause_flag, self))
            self.automation_thread.start()
            self.start_button.config(bg="green")
            self.start_button.grid_remove()

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

