# Product Image Scraper ( High Quality Images from Google )

This project contains scripts to scrape product images from Google Images and download them locally. It is divided into two main parts:
1. Scraping image URLs for product names.
2. Downloading and saving images from these URLs.

## Table of Contents
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
  - [Scraping Image URLs](#scraping-image-urls)
  - [Downloading Images](#downloading-images)
- [Logging](#logging)
- [File Structure](#file-structure)
- [Notes](#notes)

## Requirements

- Python 3.7+
- Google Chrome Browser
- [Google Chrome Driver](https://sites.google.com/a/chromium.org/chromedriver/)
- Python libraries:
  - `selenium`
  - `webdriver-manager`
  - `requests`
  - `logging`

## Setup

1. Clone the repository.

```bash
git clone https://github.com/Ansumanbhujabal/Google_Image_Scraper-High-Quality-.git
cd product-image-scraper
```

2. Install the required Python libraries.

```bash
pip install -r requirements.txt
```

3. Ensure Google Chrome is installed on your system.

4. Make sure the ChromeDriver is compatible with your Chrome browser version. You can install it via `webdriver-manager`.

## Usage

### Scraping Image URLs

This script uses Selenium to scrape URLs of product images from Google Images.

1. Prepare your input JSON file with product names. Example structure:

```json
[
    {"ITEM_NAME": "Product 1"},
    {"ITEM_NAME": "Product 2"},
    {"ITEM_NAME": "Product 3"}
]
```

2. Run the scraping script.

```bash
python scrape_images.py
```

The default filenames are:
- Input JSON: `Products_Sample.json`
- Output CSV: `Products_first_2195.csv`
- Output JSON: `Products_first_2195.json`
- Failed Cases JSON: `Products_first_2195_failed.json`

You can modify these filenames as needed.

### Downloading Images

This script downloads images from URLs obtained in the previous step.

1. Run the image downloading script.

```bash
python download_images.py
```

The default filename for the input JSON is `Products_first_44.json`. You can modify this filename as needed.

## Logging

Both scripts log their activities. The logs include detailed information about the processes and any errors encountered.

- Scraper log: `product_image_scraper.log`
- Image downloader log: `image_download.log`

## File Structure

The project directory contains the following files:

```
product-image-scraper/
│
├── scrape_images.py               # Script to scrape image URLs
├── download_images.py             # Script to download images from URLs
├── requirements.txt               # Required Python libraries
├── Products_Sample.json           # Sample input JSON file
├── product_image_scraper.log      # Log file for scraping script
├── image_download.log             # Log file for downloading script
├── successful_cases_image.json    # JSON file for successfully downloaded images
├── failed_cases_image.json        # JSON file for failed image downloads
│
└── ProductImages/                 # Directory where downloaded images are saved
```
## Sample Output
```json
[
    {"ITEM_NAME": "Mclaren F1 2025 Car"},
]
```
Output Url - "https://www.motorsportweek.com/wp-content/uploads/2024/11/file-2024-11-05T232330.165.webp"


Output Image -
![image](https://github.com/user-attachments/assets/ae3a7d5d-f975-4c52-b51d-0767c3faf48d)

## Notes

- Ensure your internet connection is stable during the scraping and downloading processes.
- The scripts include error handling and logging to help diagnose issues.
- The image downloading script includes a delay (`time.sleep(2)`) to avoid overwhelming the server with requests.

## Made By 
Ansuman SS Bhujabala
