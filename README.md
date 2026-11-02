# Upwork automation

**Demo:** [YouTube walkthrough](https://youtu.be/4ORArzjN3jg) · **Portfolio:** [aymanthefirst.github.io/portfolio](https://aymanthefirst.github.io/portfolio/)

Python + **Selenium** + **OpenAI** helper for Upwork job search: reads listings in Chrome, drafts tailored cover letters, optional GUI to review before submit.

> Personal automation tool — use only on your own Upwork account and respect Upwork’s terms.

## Stack

Python · Selenium · OpenAI API · Tkinter GUI · Chrome user profile (`upwork_profile/`)

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set `OPENAI_API_KEY`. Log into Upwork in Chrome using the persisted profile directory (created on first run).

## Run

```bash
python upwork_gui.py
```

1. Log in to Upwork and open a job search in the browser window.  
2. Click **Start** in the GUI.  
3. Review generated cover letters; choose whether to submit each application.

Main logic: `upwork_automation_script.py`.
