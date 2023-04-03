import openai
from time import sleep
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


openai.api_key = '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'

def get_elements_with_class_name(class_name):
    return driver.find_elements(By.CLASS_NAME, class_name)

def get_text_from_elements(elements):
    return [element.text for element in elements]

import re
import openai

def get_relevance_score(prompt):
    print("Getting relevance score for prompt: " + prompt)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that rates the relevance of job titles to given skills."
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

driver.get(
    "https://www.upwork.com/nx/jobs/search/?q=java&sort=recency&user_location_match=2&t=0&hourly_rate=10-&location=Americas,Europe,Oceania")
wait = WebDriverWait(driver, 10)
wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'jobs found'))

elements = get_elements_with_class_name('up-card-list-section')
text_list = get_text_from_elements(elements)

job_scores = []
print("Getting relevance scores for job titles...")
for job_title in text_list:
    prompt = f"Rate the relevance of the following job title to the skills Java, JavaScript, and Spring, on a scale of 0 to 10: '{job_title}'"
    score = get_relevance_score(prompt)
    job_scores.append((float(score), job_title))

sorted_jobs = sorted(job_scores, key=lambda x: x[0], reverse=True)[:3]

top_3_elements = [driver.find_element(By.XPATH, f"//span[contains(text(),'{job[1].split()[0]}')]") for job in sorted_jobs]


for element in top_3_elements:
    element.click()
    sleep(2)
