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

def get_text_from_anchor_elements(anchor_elements):
    return [anchor.text for anchor in anchor_elements]

def get_relevance_score(prompt):
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

options = Options()
options.add_argument("--user-data-dir=C:\\Users\\User\\Desktop\\upwork")

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
{skills}
please write a 4000 character cover letter for the following job post on upwork.com. note that this is for contract jobs a nd projects, not full time positions. Write is as ayman harake. and ommit the intro and signature. so don't say 'dear ...:
                {job_details}."""
            }
        ],
        max_tokens=200,
        temperature=0.7,
    )

    message = response.choices[0].message.content.strip()
    return message


driver.get(
    "https://www.upwork.com/nx/jobs/search/?q=java&sort=recency&user_location_match=2&t=0&hourly_rate=10-&location=Americas,Europe,Oceania")




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
    textbox.send_keys(generate_cover_letter(job_details))
    driver.back()
    print("Navigated back to job search results")
    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'jobs found'))


