import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc


def scrape_google_links(query: str, num_results: int = 10):
    
    # Set up Google search URL
    # encoded_query = urllib.parse.quote_plus(query)
    # google_url = f"search?q={encoded_query}&num={num_results}"

    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome()
    driver.get("https://www.google.com")

    # Accept cookies if prompted
    try:
        consent_button = driver.find_element(By.XPATH, '//button[contains(text(), "Accept all")]')
        consent_button.click()
    except:
        pass

    # Enter the search query
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query + Keys.RETURN)

    # Wait for results to load (adjust time if needed)
    time.sleep(25)

    # Base XPath pattern (index placeholder)
    xpath_pattern = '/html/body/div[3]/div/div[12]/div/div[2]/div[2]/div/div/div[{}]/div/div/div[1]/div/div[2]/div/div/span/a'

    found_links = []

    for i in range(1, num_results + 1):
        xpath = xpath_pattern.format(i)
        try:
            link_element = driver.find_element(By.XPATH, xpath)
            href = link_element.get_attribute("href")
            if href:
                print(f"[{i}] Found: {href}")
                found_links.append(href)
            else:
                pass
                # print(f"[{i}] Element found but href is empty.")
        except Exception as e:
            pass
            # print(f"[{i}] Could not find link at XPath: {xpath}")

    driver.quit()
    return found_links

# Example usage
if __name__ == "__main__":
    query = 'inurl:linkedin.com/in "enterprise" "@gmail" "France"'
    results = scrape_google_links(query, num_results=12)

