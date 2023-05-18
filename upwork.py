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

openai.api_key = os.environ.get('OPENAI_API_KEY')
skills = 'I have 4 years of experience in software development with a focus on Java, Spring, Spring Boot, JavaScript, HTML, CSS, Linux, Docker, Kubernetes, Selenium, Git, RESTful APIs, BASH, B2B Implementation, IT Project Solutions, Cross-functional collaboration, Multilingual skills, Project Management, Agile methodologies, Testing, BDD, TDD, Mobile Application Development, and Database Management'

current_directory = os.path.dirname(os.path.abspath(__file__))
user_data_directory = os.path.join(current_directory, 'upwork_profile')

options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--disable-dev-shm-usage')
options.add_argument(f"--user-data-dir={user_data_directory}")
options.add_argument('--headless')
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
options.add_argument('window-size=1200x600')
options.page_load_strategy = 'normal'

driver = webdriver.Chrome(options=options)
params = {
    "latitude": 0.0,
    "longitude": 0.0,
    "accuracy": 100
}
driver.execute_cdp_cmd("Page.setGeolocationOverride", params)

def close():
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.back()

def click_next_page():
    next_button = driver.find_element(By.XPATH, '//button[contains(@class, "up-pagination-item") and contains(., "Next")]')
    next_button.click()
    print("Clicked on next button")
    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'jobs found'))

def get_gpt_response(messages):
    retries = 5
    while retries > 0:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                timeout=60
            )
            return response
        except openai.error.RateLimitError as e:
            wait_seconds = int(re.search(r"Please try again in (\d+)s", str(e)).group(1))
            print(f"Rate limit reached. Waiting for {wait_seconds} seconds before retrying.")
            time.sleep(wait_seconds + 1)
        except openai.error.OpenAIError as e:
            print(f"OpenAI Error occurred: {e}")
            retries -= 1
            time.sleep(5)
    raise Exception("Unable to get a response from GPT-3.5-turbo after multiple retries.")

def get_relevance_score(prompt):
    response = get_gpt_response([
        {
            "role": "system",
            "content": f"You are a helpful assistant that rates the relevance of job titles to given skills: {skills}"
        },
        {
            "role": "user",
            "content": prompt
        }
    ])
    response_text = response['choices'][0]['message']['content'].strip()
    score = re.search(r'\d+(\.\d+)?', response_text)
    print("score:", score.group() if score else None)
    if score:
        return float(score.group())
    else:
        print("No numerical value found in the response.")
        return None

def generate_cover_letter(job_details):
    relevant_skills = ", ".join(skills.split(",")).replace("and", "").replace(" ", " ")
    south_america_mention = " Although I am currently based in the UK, I am in the process of moving to Colombia" if "america" in job_details.lower() else ""
    chatgpt_mention = "As you can see from the video that I recently made, the way I applied for this job in itself is a demonstration of my ability to do the job at hand: https://www.youtube.com/watch?v=ImustBIx4NM\n\n" if "chatgpt" in job_details.lower() else ""
    
    response = get_gpt_response([
        {
            "role": "system",
            "content": "You are a helpful assistant that writes personalized cover letters for job applications."
        },
        {
            "role": "user",
            "content": f"""Here is my CV:
{skills}
write a 200 word cover letter for the following job post. only mention the skills that I have that are relevant to the job description. do not introduce the message by mentioning the jobtitle or platform. Note that this is for contract jobs and projects, not full-time positions. Write it as Ayman Harake and omit the introduction and signature. Do not start with 'Dear Hiring Manager' or any similar salutation. Do not mention attachments, money, or the job title.{south_america_mention}. Importantly, do not claim that I have experience in anything other than what I have listed here, and make sure to only mention the skills I have listed in my CV: {relevant_skills}. Here are the job details:
                {job_details}. Do not include an introduction line. Also, do not write a paragraph that summarizes the CV."""  # Add this line here
        }
    ])

    message = response.choices[0].message.content.strip()

    while len(message.split()) > 200:
        print("Cover letter too long. Retrying with a shorter prompt.")
        response = get_gpt_response([
            {
                "role": "system",
                "content": "You are a helpful assistant that revises text to fit within a specified character limit."
            },
            {
                "role": "user",
                "content": f"Please revise the following cover letter as Ayman harake to be less than 2000 characters. remove any part that mentions the name of the jobpost. Use more than one paragraph Do not respond with anything more than the message itself: {message}"
            }
        ])
        message = response.choices[0].message.content.strip()

    message = re.sub(r"^(Dear|dear).*\n", "", message, flags=re.IGNORECASE)
    message = re.sub(r"I am writing to apply.*?\.\n", "", message, flags=re.IGNORECASE)
    message = message.lstrip()
    message = chatgpt_mention + message
    return message




driver.get(
    "https://www.upwork.com/nx/jobs/search/?q=java&sort=recency&user_location_match=2&duration_v3=months,semester,ongoing&location=Australia%20and%20New%20Zealand,Northern%20America,Northern%20Europe,Southern%20Europe,Western%20Europe")

wait = WebDriverWait(driver, 10)
wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'jobs found'))

while True:
    job_count = len(driver.find_elements(By.CLASS_NAME, 'up-card-list-section'))
    for index in range(job_count):
        jobs = driver.find_elements(By.CLASS_NAME, 'up-card-list-section')
        job = jobs[index]

        job = jobs[index]
        job_title = job.text
        if 'applied' in job_title.lower():
            print("Job already applied. Skipping...")
            continue
        if 'less than a month' in job_title.lower():
            print("Job posted less than a month ago. Skipping...")
            continue
        budget = re.search(r'Est. Budget: \$([\d,]+)', job_title)
        if budget and int(budget.group(1).replace(',', '')) < 600:
            print("Budget is less than $600. Skipping...")
            continue
        prompt = f"Rate the relevance of the following job title '{job_title}' to the skills and experience mentioned in this CV: '{skills}'. Please answer in a numerical value and give no more words than the one value."
        score = get_relevance_score(prompt)
        if score >= 9 or score >= 9.0:
            # apply for job
            wait = WebDriverWait(driver, 10) 
            job.click()
            print("Clicked on job title")
            wait.until(lambda driver: EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'Submit Proposal')(driver) or EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'Apply Now')(driver))
            if 'applied' in driver.find_element(By.TAG_NAME, 'body').text:
                close()
                continue
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
            job_details = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'fe-job-details'))).text
            textbox.send_keys(generate_cover_letter(job_details))
            time.sleep(5)
            close()
            print("Navigated back to job search results")
            wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'jobs found'))
    click_next_page()
    time.sleep(5)
    jobs = driver.find_elements(By.CLASS_NAME, 'up-card-list-section')
