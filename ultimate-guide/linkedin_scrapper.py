import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import urllib.parse
import csv


def scrape_google_links(query: str, num_results: int = 10):
    
    # Set up Google search URL
    encoded_query = urllib.parse.quote_plus(query)
    google_url = f"https://www.google.com/search?q={encoded_query}&num={num_results}"

    options = Options()
    
    
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(options=options)
    driver.get(google_url)

    # Accept cookies if prompted
    try:
        consent_button = driver.find_element(By.XPATH, '//button[contains(text(), "Accept all")]')
        consent_button.click()
    except:
        pass

    # Enter the search query
    # search_box = driver.find_element(By.NAME, "q")
    # search_box.send_keys(query + Keys.RETURN)

    # Wait for results to load (adjust time if needed)
    time.sleep(40)

    result_blocks = driver.find_elements(By.CSS_SELECTOR, 'div.kb0PBd.A9Y9g.jGGQ5e')
    
    results = []
    
    for block in result_blocks:
        try:
            a_tag = block.find_element(By.CSS_SELECTOR, 'a')
            link = a_tag.get_attribute("href")

            desc_tag = block.find_element(By.TAG_NAME, 'span')  # metadata/snippet
            description = desc_tag.text.strip()

            # Extract email if present
            email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", description)
            email = email_match.group(0) if email_match else "NaN"

            if link:
                results.append({
                    'link': link,
                    'email': email
                })
                print(f"[{len(results)}] {link}\n    {email}\n\n")

            if len(results) >= num_results:
                break
        
        except Exception as e:
            print("Error: ", e)
            continue

    driver.quit()
    return results


# Example usage
# if __name__ == "__main__":
#     query = 'inurl:linkedin.com/in "@outlook.fr " "contact"'
#     results = scrape_google_links(query, num_results=17)

#     # Write results to a CSV file
#     with open("google_results.csv", mode="w", newline="", encoding="utf-8") as file:
#         writer = csv.DictWriter(file, fieldnames=["link", "email"])
#         writer.writeheader()
#         writer.writerows(results)

#     print(f"\nSaved {len(results)} results to 'google_results.csv'")

