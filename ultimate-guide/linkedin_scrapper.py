import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import urllib.parse
import csv
from bs4 import BeautifulSoup


def extract_email_from_text(text):

    text = re.sub(r'\s*@\s*', '@', text)  # Remove space around @
    # Now extract email
    match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    return match.group(0) if match else "NaN"


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
    time.sleep(50)

    result_blocks = driver.find_elements(By.CSS_SELECTOR,'div.N54PNb.BToiNc')
    print("Number of blocks found: ", len(result_blocks))
    results = []
    
    for block in result_blocks:
        # print("Block: ", block)
        try:
            a_tag = block.find_element(By.CSS_SELECTOR, 'a')
            link = a_tag.get_attribute("href")
            print("Link: ", link)

            metadata_html = ""
            description_html = ""
            
            
            try:
                metadata = block.find_element(By.CSS_SELECTOR, 'div.YrbPuc')
                metadata_html = metadata.get_attribute("outerHTML")
            except Exception as e:
                pass

            try:
                description = block.find_element(By.CSS_SELECTOR, 'div.VwiC3b')
                description_html = description.get_attribute("outerHTML")
            except Exception as e:
                pass


            # --- Combine and parse both ---
            full_html = metadata_html + description_html
            soup = BeautifulSoup(full_html, "html.parser")
            text = soup.get_text(separator=" ", strip=True)
            print("Full text:", text)


            email = extract_email_from_text(text)
            print("Email: ", email)
            print()
            

            if link:
                results.append({
                    'link': link,
                    'email': email,
                })

            if len(results) >= num_results:
                break
        
        except Exception as e:
            print("Error: ", e)
            continue

    driver.quit()
    return results


# Example usage
if __name__ == "__main__":
    query = 'inurl:linkedin.com/in "@gmail.com " "coach"'
    results = scrape_google_links(query, num_results=15)

    # Write results to a CSV file
    with open("results.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["link", "email"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\nSaved {len(results)} results to 'results.csv'")

