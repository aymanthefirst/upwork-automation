from datetime import datetime
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
import time
import os
import openai
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from tkinter import messagebox
import traceback
import pygame
import upwork_gui
import datetime
import os

openai.api_key = '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'
skills = 'I have 4 years of experience in software development with a focus on Java, python, chatgpt, GPT, artificial intelligence, Spring, Spring Boot, JavaScript, HTML, CSS, Linux, Docker, Kubernetes, Selenium, Git, RESTful APIs, BASH, B2B Implementation, IT Project Solutions, Cross-functional collaboration, Multilingual skills, Project Management, Agile methodologies, Testing, BDD, TDD, Mobile Application Development, and Database Management'

current_directory = os.path.dirname(os.path.abspath(__file__))
user_data_directory = os.path.join(current_directory, 'upwork_profile')

options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--disable-dev-shm-usage')
options.add_argument(f"--user-data-dir={user_data_directory}")

options.page_load_strategy = 'normal'

driver = webdriver.Chrome(options=options)
params = {
    "latitude": 0.0,
    "longitude": 0.0,
    "accuracy": 100
}
driver.execute_cdp_cmd("Page.setGeolocationOverride", params)

current_session_file_name = None
def save_cover_letter_to_file(job_title, cover_letter):
    global current_session_file_name

    previous_sessions_folder = "previous_sessions"
    if not os.path.exists(previous_sessions_folder):
        os.makedirs(previous_sessions_folder)

    if current_session_file_name is None:
        current_session_file_name = f"cover_letters_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

    file_path = os.path.join(previous_sessions_folder,
                             current_session_file_name)

    with open(file_path, "a") as file:
        file.write(f"Job Title: {job_title}\n")
        file.write(
            f"Date and Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write("Cover Letter:\n")
        file.write(cover_letter)
        file.write("\n\n---\n\n")

prompt_on_close = False
def close_with_prompt(ask_continue=None, gui_instance=None):
    global prompt_on_close

    if prompt_on_close:  
        sound_file = 'chime.wav'
        play_sound(sound_file)
        user_choice = messagebox.askyesno(
            "Submit Application?", "Do you want to submit the application?")
    else:
        user_choice = True  

    if user_choice:
        submit_button = driver.find_element(
            By.XPATH, "//button[contains(., 'send') or contains(., 'Send')]")
        submit_button.click()
        gui_instance.add_one_submit()
        try:
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element(
                (By.TAG_NAME, 'body'), 'Your proposal was submitted.'))
        except:
            print('Error in submitting application. Skipping...')
            messagebox.showerror(
                "Error", "Error in submitting application. Please manually submit it, then click ok to continue.")
            close()
            return True
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.back()


def play_sound(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def close():
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.back()

def get_keywords_to_avoid():
    with open("keywords_to_avoid.txt", "r") as file:
        keywords = file.read()
    return keywords.split(',')


def apply(job, auto_generate_cover_letter, gui_instance):
    wait = WebDriverWait(driver, 10) 
    job.click()
    print("Clicked on job title")
    wait.until(lambda driver: EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'Submit Proposal')(driver) or EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'Apply Now')(driver))
    if 'applied' in driver.find_element(By.TAG_NAME, 'body').text:
        print("Job already applied. Skipping...")
        driver.back()
        return True
    if 'submitted' in driver.find_element(By.TAG_NAME, 'body').text:
            print("Job already applied. Skipping...")
            driver.back()
            return True    
    if "You do not meet all the client's preferred qualifications" in driver.find_element(By.TAG_NAME, 'body').text:
        print("You do not meet all the client's preferred qualifications. Skipping...")
        driver.back()
        return True
    print("Found 'Apply Now' button")
    apply_now_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Apply Now"]'))
    )
    apply_now_button.click()
    driver.switch_to.window(driver.window_handles[-1])
    textbox = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, '//textarea[@aria-labelledby="cover_letter_label"]'))
    )
    try:
        nowrap_element = driver.find_element(By.CLASS_NAME, 'up-truncation-label').click()
        print('clicked on more button')
    except ElementNotInteractableException:
        nowrap_element = None
        print("More button not found")
    try:
        if auto_generate_cover_letter:
            exit_if_multiple_textboxes()
    except ValueError as ve:
        print(str(ve))
        close()
        return True
    job_details = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'fe-job-details'))).text
    if auto_generate_cover_letter:
        textbox.send_keys(generate_cover_letter(job_details, gui_instance))
        time.sleep(5)
    else:
        print("Auto-generating cover letter is disabled.")
        print("Please manually enter your cover letter into the website and submit it.")

    with open("urls.txt", "a") as file:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{driver.current_url} - Captured on: {current_time}\n")



    time.sleep(5)
    close_with_prompt(gui_instance=gui_instance)
    print("Navigated back to job search results")
    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'jobs found'))

def click_next_page():
    next_button = driver.find_element(By.XPATH, '//button[contains(@class, "up-pagination-item") and contains(., "Next")]')
    next_button.click()
    print("Clicked on next button")
    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'jobs found'))

def exit_if_multiple_textboxes():
    textareas = driver.find_elements(By.TAG_NAME, 'textarea')
    if len(textareas) > 1:
        print('More than one textarea on the page. Skipping job...')
        raise ValueError("More than one textarea on the page.")
    
def should_skip_job(job_title, keywords_to_avoid):
    for keyword in keywords_to_avoid:
        keyword = keyword.strip().lower()
        if keyword and keyword in job_title.lower():
            print(f"Keyword '{keyword}' found in job title. Skipping...")
            return True
    return False


def get_gpt_response(messages, gui_instance=None):
    global token_counter
    retries = 5
    while retries > 0:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                timeout=60
            )
            token_counter += response['usage']['total_tokens']
            if gui_instance:
                gui_instance.update_tokens_used(token_counter)
            return response
        except openai.error.RateLimitError as e:
            wait_seconds = int(
                re.search(r"Please try again in (\d+)s", str(e)).group(1))
            print(
                f"Rate limit reached. Waiting for {wait_seconds} seconds before retrying.")
            time.sleep(wait_seconds + 1)
        except openai.error.OpenAIError as e:
            print(f"OpenAI Error occurred: {e}")
            retries -= 1
            time.sleep(5)
    raise Exception(
        "Unable to get a response from GPT-3.5-turbo after multiple retries.")


def get_relevance_score(prompt, gui_instance=None):
    response = get_gpt_response([
        {
            "role": "system",
            "content": f"You are a helpful assistant that rates the relevance of job titles to given skills: {skills}"
        },
        {
            "role": "user",
            "content": prompt
        }
    ], gui_instance)  
    response_text = response['choices'][0]['message']['content'].strip()
    score = re.search(r'\d+(\.\d+)?', response_text)
    print("score:", score.group() if score else None)
    if score:
        return float(score.group())
    else:
        print("No numerical value found in the response.")
        return None


def generate_cover_letter(job_details, gui_instance=None):
    def generate_message(prompt, gui_instance=None):
        response = get_gpt_response(prompt, gui_instance)
        message = response.choices[0].message.content.strip()
        return message

    south_america_mention = " Although I am currently based in the UK, I am in the process of moving to Colombia" if "america" in job_details.lower() else ""
    chatgpt_mention = "As you can see from the video that I recently made, the way I applied for this job in itself is a demonstration of my ability to do the job at hand: https://www.youtube.com/watch?v=ImustBIx4NM\n\n" if "gpt" in job_details.lower() else ""
    money_back_guarantee = "Although I have 4 years of experience in software development, I am new to the Upwork platform, so I understand that choosing me might feel like a risk for you. To minimize this risk and demonstrate my confidence in my abilities, I am offering a money-back guarantee policy. If you are not satisfied with my work, I will provide a full or partial refund, depending on your preference, without any questions.\n\n"

    prompt = [
        {
            "role": "system",
            "content": "You are a helpful assistant that writes personalized cover letters for job applications."
        },
        {
            "role": "user",
            "content": f"""Please write a concise cover letter with a maximum of 200 words.
            Write it as Ayman Harake.
            Do not mention attachments, money, or the job title.
            My skills: {skills}
            job details: {job_details}"""
        }
    ]

    while True:
        message = generate_message(prompt, gui_instance)

        if len(message.split()) <= 200:
            break
        else:
            print("Cover letter too long. Retrying with the same prompt.")

    message = re.sub(r"^(Dear|dear).*\n", "", message, flags=re.IGNORECASE)
    message = message.lstrip()
    message = "Hi, \n\n" + message
    paragraphs = message.split('\n\n')
    paragraphs = [p for p in paragraphs if 'attached' not in p.lower()]
    message = '\n\n'.join(paragraphs)

    if len(paragraphs) > 2:
        additional_mentions = chatgpt_mention + \
        south_america_mention + money_back_guarantee
        paragraphs[2] = additional_mentions + paragraphs[2]
        message = '\n\n'.join(paragraphs)

    save_cover_letter_to_file(job_details, message)
    return message



driver.get(
    "https://www.upwork.com/nx/jobs/search/?sort=recency&user_location_match=2&or_terms=gpt%20java&t=0,1&client_hires=1-9,10-&proposals=0-4,5-9,10-14,15-19,20-49&amount=1000-4999,5000-&hourly_rate=25-")

wait = WebDriverWait(driver, 10)
wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'jobs found'))


def run_automation(auto_generate_cover_letter, stop_flag, pause_flag, gui_instance):
    global token_counter
    token_counter = 0
    applied_count = 0
    application_limit = 10

    if gui_instance is not None:
        application_limit = gui_instance.application_limit

    
    search_page_url = driver.current_url

    while not stop_flag():
        try:
            job_count = len(driver.find_elements(
                By.CLASS_NAME, 'up-card-list-section'))
            for index in range(job_count):
                gui_instance.update_tokens_used(token_counter)
                try:
                    keywords_to_avoid = get_keywords_to_avoid()
                    jobs = driver.find_elements(
                        By.CLASS_NAME, 'up-card-list-section')
                    job = jobs[index]
                    job_title = job.text
                    budget = re.search(r'Est. Budget: \$([\d,]+)', job_title)
                    if budget and int(budget.group(1).replace(',', '')) < 600:
                        print("Budget is less than $600. Skipping...")
                        continue
                    if should_skip_job(job_title, keywords_to_avoid):
                        continue
                    prompt = f"Rate the relevance of the following job title '{job_title}' to the skills and experience mentioned in this CV: '{skills}'. Please answer in a numerical value and give no more words than the one value."
                    score = get_relevance_score(
                        prompt, gui_instance=gui_instance)
                    if score >= 9 or score >= 9.0:
                        should_continue = apply(
                            job, auto_generate_cover_letter, gui_instance)
                        if should_continue:
                            continue
                        applied_count += 1
                        if applied_count >= application_limit:
                            print(
                                f"Application limit of {application_limit} reached.")
                            return
                except Exception as e:
                    print(f"Error occurred during job application: {e}")
                    traceback.print_exc()
                    with open("error.log", "a") as f:
                        f.write(
                            f"Error occurred during job application: {e}\n")
                        f.write(f"Job details: {job_title}\n")
                        f.write(f"Job URL: {driver.current_url}\n\n")
                    driver.get(search_page_url)  
                    time.sleep(5)  
                    continue
            click_next_page()
            time.sleep(5)
            jobs = driver.find_elements(By.CLASS_NAME, 'up-card-list-section')
        except Exception as e:
            print(str(e))
            traceback.print_exc()
            driver.get(search_page_url)  
            time.sleep(5)  
