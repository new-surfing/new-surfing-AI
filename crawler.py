import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def crawl_article_content(url):
    max_attempts = 2

    for attempt in range(max_attempts):
        driver = None
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

            driver = webdriver.Chrome(options=options)
            driver.get(url)

            try:
                content = driver.find_element(By.CSS_SELECTOR, 'div.detail-body.font-size')
                return content.text
            except NoSuchElementException:
                content = driver.find_element(By.TAG_NAME, 'body')
                return content.text
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(1)  
        finally:
            if driver:
                driver.quit()

    print("Failed to crawl the article after maximum attempts")
    return None
