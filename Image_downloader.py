import os
import json
import logging
import requests
import time

# Directories & File Paths
IMAGE_DIR = "ProductImages"
FAILED_CASES_FILE = "failed_cases_image.json"
SUCCESSFUL_CASES_FILE = "successful_cases_image.json"
LOG_FILE = "image_download.log"

# Ensure the image directory exists
os.makedirs(IMAGE_DIR, exist_ok=True)

# Setup logging (both to console and log file)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def sanitize_filename(product_name):
    """Sanitize product name to create a valid filename."""
    return product_name.replace(" ", "_").replace("/", "_").replace("|", "_").replace("-", "_")

def download_image(product, image_url):
    """Download and save image."""
    try:
        response = requests.get(image_url, stream=True, timeout=10)
        time.sleep(2)
        response.raise_for_status()
        
        # Get file extension from URL or default to .jpg
        file_extension = os.path.splitext(image_url.split("?")[0])[-1].lower()
        if file_extension not in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
            file_extension = ".jpg"
        
        filename = sanitize_filename(product) + file_extension
        file_path = os.path.join(IMAGE_DIR, filename)

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        
        logging.info(f"✅ Downloaded: {product} -> {file_path}")
        return file_path
    except Exception as e:
        logging.error(f"❌ Failed to download {product}: {e}")
        return None

def append_case(file_path, case_data):
    """Append case data to a JSON file without overwriting previous entries."""
    cases = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                cases = json.load(f)
                if not isinstance(cases, list):
                    cases = []
            except json.JSONDecodeError:
                cases = []
    
    cases.append(case_data)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(cases, f, indent=4)
    logging.info(f"🔄 Updated {file_path} with: {case_data}")

def process_images(json_file):
    """Process images one by one from JSON file."""
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    logging.info(f"📂 Processing {len(data)} items from {json_file}")
    
    for item in data:
        product = item.get("Product")
        image_url = item.get("image_url")
        
        if not product or not image_url:
            logging.warning(f"⚠️ Skipping invalid entry: {item}")
            continue
        
        file_path = download_image(product, image_url)
        if file_path:
            append_case(SUCCESSFUL_CASES_FILE, {"Product": product, "image_path": file_path})
        else:
            append_case(FAILED_CASES_FILE, {"Product": product, "image_url": image_url})
    
    logging.info("🎉 Image processing completed!")

if __name__ == "__main__":
    process_images("Wmart_Products_first_44.json")

