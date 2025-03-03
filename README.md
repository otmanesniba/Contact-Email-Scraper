# Contact Email Scraper


A Python script to scrape contact emails from websites using **Pyppeteer** (a headless browser automation tool). The script navigates to URLs provided in a file, searches for "Contact" links, and extracts email addresses from the pages.

---

## **Features**
- **Headless Browser Automation**: Uses Pyppeteer to scrape dynamic web pages.
- **Contact Page Detection**: Automatically navigates to "Contact" pages if available.
- **Email Extraction**: Extracts email addresses using regex.
- **File Input/Output**: Reads URLs from a file and saves extracted emails to a text file on your desktop.
- **User-Friendly**: Displays a colorful ASCII banner and progress updates in the terminal.

---

## **Prerequisites**
Before running the script, ensure you have the following:
1. **Python 3.8+** installed.
2. Required Python libraries installed. You can install them using:

    ```bash
   pip install pyppeteer pyfiglet termcolor
