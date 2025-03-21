import time
import json
import logging
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager



def setup_logger():
    logging.basicConfig(
        filename="product_image_scraper.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

def get_google_image_url(query):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--lang=en-US")
    chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})
    # chrome_options.add_argument(
    # "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    # )


    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.set_window_size(1280, 720)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    try:
        search_url = f"https://www.google.com/search?tbm=isch&q={query.replace(' ', '+')}"
        driver.get(search_url)
        time.sleep(5)
        
        try:
            driver.find_element(By.XPATH, "//div[text()='Accept all']").click()
            time.sleep(5)
        except:
            pass
        
        first_image = driver.find_element(By.CSS_SELECTOR, "div.F0uyec")
        first_image.click()
        time.sleep(5)
        
        main_image = driver.find_element(By.CSS_SELECTOR, "img.sFlh5c")
        image_url = main_image.get_attribute("src")
        
        return image_url
    
    except Exception as e:
        logging.error(f"Error fetching image for query '{query}': {e}")
        return None
    
    finally:
        driver.quit()

def process_items(input_json, output_csv_path, output_json_path, failed_cases_path):
    with open(input_json, "r", encoding="utf-8") as f:
        items = json.load(f)
    
    results = []
    failed_cases = []
    
    with open(output_csv_path, "w", newline="", encoding="utf-8") as csvfile, \
         open(output_json_path, "w", encoding="utf-8") as jsonfile, \
         open(failed_cases_path, "w", encoding="utf-8") as failed_jsonfile:
        
        writer = csv.DictWriter(csvfile, fieldnames=["Product", "image_url"])
        writer.writeheader()
        
        jsonfile.write("[\n")  # Start JSON array
        first_entry = True

        for item in items:
            query = item.get("ITEM_NAME")
            logging.info(f"Processing: {query}")
            image_url = get_google_image_url(query)

            if image_url:
                result = {"Product": query, "image_url": image_url}
                results.append(result)
                writer.writerow(result)

                # Append to JSON without rewriting the entire file
                if not first_entry:
                    jsonfile.write(",\n")
                json.dump(result, jsonfile)
                first_entry = False

            else:
                failed_case = {"Product": query, "error": "Failed to retrieve image"}
                failed_cases.append(failed_case)
        
        jsonfile.write("\n]")  # Close JSON array

        json.dump(failed_cases, failed_jsonfile, indent=4)
    
    logging.info("Processing complete. Output saved.")

if __name__ == "__main__":
    setup_logger()
    process_items("Wmart_Products_Sample.json", "Wmart_Products_first_2195.csv", "Wmart_Products_first_2195.json", "Wmart_Products_first_2195_failed.json")
