import re
import openai
import traceback
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
print('Imported libraries')

try:
    openai.api_key = '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'
    print('OpenAI API key set to: ' + openai.api_key)
except KeyError:
    exit(1)

def sendKeys(textToSend):
    print('send keys')
    wait = WebDriverWait(driver, 10)
    textBox = wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'textarea')))
    textBox.clear()
    textBox.send_keys(textToSend)
    textBox.send_keys(Keys.ENTER)
    sleep(2)

def getBodyText():
    print('get body text')
    wait = WebDriverWait(driver, 10)
    cardContainer = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'profileCard__card')))
    profile_text = cardContainer.text
    # Remove emojis and other non-text characters
    profile_text = re.sub(r'[^\x00-\x7F]+', '', profile_text)
    return profile_text

def generateMessage():
    print('generate message')
    try:
        # Get the profile description
        profile_description = getBodyText()

        # Define the message objects for the OpenAI API
        messages = [
            {
                "content": f"Analyze the following profile description and craft a personalized first Tinder message. Here are the rules for your response:\n- Do not include any placeholders like [name] or [her name] in your response\n- Do not include any brackets or parenthesis in your response\n- Respond in less than 40 words.\n- do not offer meet up in any way\n- Contain the question 'are you as tall as you look?'.\n- Sound natural and engaging.\n- Don't mention anything to do with relationship goals.\n- Profile description: {profile_description}",
                "role": "user"
            }
        ]

        # Generate the message using OpenAI GPT-3 API
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=messages,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )
        message = response.choices[0]['text'].strip()
    except Exception as e:
        print("Error in generateMessage():")
        traceback.print_exc()

    return message

print('Ssetting options')
options = Options()
# options.add_argument("--headless")
options.add_argument("--user-data-dir=C:\\Users\\User\\Desktop\\upwork")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")  # Disabling GPU can help with some issues in headless mode
options.add_argument("--no-sandbox")  # Bypass OS security model, required for some systems
options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
print('Options set')

# Add headers to simulate a real browser
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

print('Getting url')
driver.get(
    "https://www.upwork.com/nx/jobs/search/?q=java&sort=recency&user_location_match=2&t=0&hourly_rate=10-&location=Americas,Europe,Oceania")
wait = WebDriverWait(driver, 10)
print('Got url')
wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'jobs found'))

def get_relevance_score(prompt):
    print("Getting relevance score for prompt: " + prompt)
    # Use the OpenAI GPT-3 API to generate a relevance score for the given prompt
    response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )

    # Extract the relevance score from the API response
    score = response.choices[0].text.strip()

    return score

while True:
    print("Waiting for jobs to load...")
    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'jobs found'))

    # Extract job titles from the body text
    print("Extracting job titles...")
    body_text = driver.find_element(By.TAG_NAME, 'body').text
    job_titles = [line.strip() for line in body_text.split('\n') if line.strip()]

    # Get relevance scores for each job title
    job_scores = []
    print("Getting relevance scores for job titles...")
    for job_title in job_titles:
        prompt = f"Rate the relevance of the following job title to the skills Java, JavaScript, and Spring, on a scale of 0 to 10: '{job_title}'"
        score = get_relevance_score(prompt)
        job_scores.append((score, job_title))

    # Sort jobs based on relevance scores and only consider the top 3
    print("Sorting job titles...")
    sorted_jobs = sorted(job_scores, key=lambda x: x[0], reverse=True)[:3]

    for score, job_title in sorted_jobs:
        try:
            title_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(),'{job_title}')]")))
            print(f"Found job title: {title_element.text}")
            title_element.click()
            print("Clicked on job title")

            wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'Submit Proposal'))
            print("Found 'Apply Now' button")

            # Go back to the previous page
            driver.back()
            print("Navigated back to job search results")
            wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'jobs found'))
        except Exception as e:
            print(f"Exception occurred: {e}")
            traceback.print_exc()
            continue
    break