import time
import os
import openai
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

openai.api_key = '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'
skills = 'I have 4 years of experience in software development with a focus on Java, Spring, Spring Boot, JavaScript, HTML, CSS, Linux, Docker, Kubernetes, Selenium, Git, RESTful APIs, BASH, B2B Implementation, IT Project Solutions, Cross-functional collaboration, Multilingual skills, Project Management, Agile methodologies, Testing, BDD, TDD, Mobile Application Development, and Database Management'


def get_anchor_elements_within_class_name(class_name):
    elements = driver.find_elements(By.CLASS_NAME, class_name)
    anchor_elements = [element.find_element(By.TAG_NAME, 'a') for element in elements]
    return anchor_elements

def get_more_button():
    buttons = driver.find_elements(By.CLASS_NAME, "up-btn-link")
    for button in buttons:
        if button.text.lower() == "more":
            return button
    return None

def get_text_from_anchor_elements(anchor_elements):
    return [anchor.text for anchor in anchor_elements]


def get_relevance_score(prompt):
    while True:
        try:
            print("Getting relevance score for prompt: " + prompt)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a helpful assistant that rates the relevance of job titles to given skills: {skills}"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            response_text = response['choices'][0]['message']['content'].strip()

            score = re.search(r'\d+(\.\d+)?', response_text)
            if score:
                return float(score.group())
            else:
                print("No numerical value found in the response.")
                return None
        except openai.error.RateLimitError as e:
            wait_seconds = int(re.search(r"Please try again in (\d+)s", str(e)).group(1))
            print(f"Rate limit reached. Waiting for {wait_seconds} seconds before retrying.")
            time.sleep(wait_seconds + 1)  # Add 1 second to ensure the rate limit has reset





current_directory = os.path.dirname(os.path.abspath(__file__))
user_data_directory = os.path.join(current_directory, 'upwork_profile')


options = Options()
options.add_argument(f"--user-data-dir={user_data_directory}")

options.page_load_strategy = 'normal'

driver = webdriver.Chrome(options=options)
params = {
    "latitude": 0.0,
    "longitude": 0.0,
    "accuracy": 100
}
driver.execute_cdp_cmd("Page.setGeolocationOverride", params)

def generate_cover_letter(job_details):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that writes personalized cover letters for job applications."
            },
            {
                "role": "user",
                "content": f"""Here is my CV:
I have 4 years of experience in software development with a focus on Java, Spring, Spring Boot, JavaScript, HTML, CSS, Linux, Docker, Kubernetes, Selenium, Git, RESTful APIs, BASH, B2B Implementation, IT Project Solutions, Cross-functional collaboration, Multilingual skills, Project Management, Agile methodologies, Testing, BDD, TDD, Mobile Application Development, and Database Management,
please write a cover letter with no more than 4000 characters for the following job post on upwork.com. Note that this is for contract jobs and projects, not full-time positions. Write it as Ayman Harake and omit the introduction and signature. Do not start with 'Dear Hiring Manager' or any similar salutation:
                {job_details}."""
            }
        ],
        temperature=0.7,
    )

    message = response.choices[0].message.content.strip()
    # Limit the message to 4000 characters, minus 1 to account for potential newline character
    message = message[:3999]
    # Remove any leading salutation
    message = re.sub(r"^(Dear|dear).*\n", "", message, flags=re.IGNORECASE)
    message = message.lstrip()
    return message

driver.get(
    "https://www.upwork.com/nx/jobs/search/?q=java&sort=recency&user_location_match=2&ontology_skill_uid=1031626782313791488&location=Americas,Europe,Oceania")




wait = WebDriverWait(driver, 10)
wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'jobs found'))

anchor_elements = get_anchor_elements_within_class_name('up-card-list-section')

text_list = get_text_from_anchor_elements(anchor_elements)

job_scores = []
print("Getting relevance scores for job titles...")
for job_title in text_list:
    prompt = f"Rate the relevance of the following job title to the skills and experience mentioned in this CV: '{skills}'."
    score = get_relevance_score(prompt)
    if score is not None:  # Add this check to prevent adding None values
        job_scores.append((float(score), job_title))

sorted_jobs = sorted(job_scores, key=lambda x: x[0], reverse=True)[:3]

top_3_elements = [driver.find_element(By.XPATH, f"//a[contains(text(),'{job[1].split()[0]}')]") for job in sorted_jobs]

for idx, element in enumerate(top_3_elements):
    xpath_string = f"//a[contains(text(),'{sorted_jobs[idx][1].split()[0]}')]"
    wait = WebDriverWait(driver, 10)  # Adjust the waiting time (10 seconds here) if necessary
    clickable_element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_string)))
    clickable_element.click()
    print("Clicked on job title")
    wait.until(lambda driver: EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'Submit Proposal')(driver) or EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'Apply Now')(driver))
    print("Found 'Apply Now' button")
    apply_now_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Apply Now"]'))
    )
    apply_now_button.click()
    driver.switch_to.window(driver.window_handles[-1])
    textbox = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, '//textarea[@aria-labelledby="cover_letter_label"]'))
    )
    job_details = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'fe-job-details'))).text
    more_button = get_more_button()
    more_button.click()
    textbox.send_keys(generate_cover_letter(job_details))
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.back()
    print("Navigated back to job search results")
    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'jobs found'))


