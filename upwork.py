import openai
from time import sleep
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import re
import time

openai.api_key = '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'

# def get_anchor_elements_within_class_name(class_name):
#     elements = driver.find_elements(By.CLASS_NAME, class_name)
#     anchor_elements = [element.find_element(By.TAG_NAME, 'a') for element in elements]
#     return anchor_elements

# def get_text_from_anchor_elements(anchor_elements):
#     return [anchor.text for anchor in anchor_elements]

# def get_relevance_score(prompt):
#     print("Getting relevance score for prompt: " + prompt)
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are a helpful assistant that rates the relevance of job titles to given skills."
#             },
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ]
#     )
#     response_text = response['choices'][0]['message']['content'].strip()
    
#     score = re.search(r'\d+(\.\d+)?', response_text)
#     if score:
#         return float(score.group())
#     else:
#         print("No numerical value found in the response.")
#         return None

options = Options()
options.add_argument("--user-data-dir=C:\\Users\\User\\Desktop\\upwork")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
options.page_load_strategy = 'normal'

driver = webdriver.Chrome(options=options)
params = {
    "latitude": 0.0,
    "longitude": 0.0,
    "accuracy": 100
}
driver.execute_cdp_cmd("Page.setGeolocationOverride", params)

def generate_cover_letter():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that writes personalized cover letters for job applications."
            },
            {
                "role": "user",
                "content": (
                    "Write a personalized cover letter for a Java Developer position "
                    "highlighting the following skills and experiences: "
                    "Java, Spring, Spring Boot, JavaScript, HTML, CSS, Linux, Docker, Kubernetes, "
                    "Selenium, Git, RESTful APIs, BASH, B2B Implementation, IT Project Solutions, "
                    "Cross-functional collaboration, Multilingual skills, Project Management, "
                    "Agile methodologies, Testing, BDD, TDD, Mobile Application Development, "
                    "and Database Management."
                )
            }
        ],
        max_tokens=200,
        temperature=0.7,
    )

    message = response.choices[0].message.content.strip()
    return message


driver.get(
    "https://www.upwork.com/nx/jobs/search/?q=java&sort=recency&user_location_match=2&t=0&hourly_rate=10-&location=Americas,Europe,Oceania")
# wait = WebDriverWait(driver, 10)
# wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'jobs found'))

# anchor_elements = get_anchor_elements_within_class_name('up-card-list-section')
# text_list = get_text_from_anchor_elements(anchor_elements)

# job_scores = []
# print("Getting relevance scores for job titles...")
# for job_title in text_list:
#     prompt = f"""Rate the relevance of the following job title to the skills and experience mentioned in this CV: '{job_title}'.
#     Skills: Java, Spring, Spring Boot, JavaScript, HTML, CSS, Linux, Docker, Kubernetes, Selenium, Git, RESTful APIs, BASH, B2B Implementation, IT Project Solutions, Cross-functional collaboration, Multilingual skills, Project Management, Agile methodologies, Testing, BDD, TDD, Mobile Application Development, Database Management."""
#     score = get_relevance_score(prompt)
#     job_scores.append((float(score), job_title))

# sorted_jobs = sorted(job_scores, key=lambda x: x[0], reverse=True)[:3]

# # ... (Continued from the previous part of the code)

# top_3_elements = [driver.find_element(By.XPATH, f"//a[contains(text(),'{job[1].split()[0]}')]") for job in sorted_jobs]

# for idx, element in enumerate(top_3_elements):
#     # Create the XPath string for the clickable element
#     xpath_string = f"//a[contains(text(),'{sorted_jobs[idx][1].split()[0]}')]"

#     # Use WebDriverWait to wait for the element to be clickable
#     wait = WebDriverWait(driver, 10)  # Adjust the waiting time (10 seconds here) if necessary
#     clickable_element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_string)))
#     clickable_element.click()
#     print("Clicked on job title")
    # wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'Submit Proposal'))
print("Found 'Apply Now' button")
# Wait for the button with the specified aria-label to become clickable
apply_now_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Apply Now"]'))
)
# Click the button
apply_now_button.click()



driver.switch_to.window(driver.window_handles[-1])






textbox = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.XPATH, '//textarea[@aria-labelledby="cover_letter_label"]'))
)
textbox.send_keys(generate_cover_letter())

driver.back()
print("Navigated back to job search results")
wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'jobs found'))


