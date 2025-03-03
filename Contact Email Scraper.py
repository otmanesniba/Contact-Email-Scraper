import asyncio
from pyppeteer import launch
import re
import os
import pyfiglet
from termcolor import colored

def print_banner():
    # Generate ASCII banner for "CONTACT EMAILS"
    ascii_banner = pyfiglet.figlet_format("CONTACT EMAILS")
    print(colored(ascii_banner, "cyan"))  # Print in cyan
    print(colored("Made by Otmane Sniba", "cyan"))

async def scrape_emails_with_pyppeteer(urls):
    # Launch the browser with the specified Edge path
    browser = await launch(
        headless=True, 
        executablePath="C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"  # Update this path if needed
    )
    all_emails = []

    for url in urls:
        print(colored(f"Scraping {url}...", "green"))
        try:
            page = await browser.newPage()
            await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.48")
            await page.goto(url, {"waitUntil": "networkidle2"})

            # Search for "Contact" links
            contact_links = await page.evaluate('''() => {
                return Array.from(document.querySelectorAll('a'))
                            .filter(a => a.textContent.toLowerCase().includes('contact'))
                            .map(a => a.href);
            }''')

            if contact_links:
                print(colored("Found Contact page links, navigating...", "blue"))
                for contact_url in contact_links:
                    try:
                        await page.goto(contact_url, {"waitUntil": "networkidle2"})
                    except Exception as e:
                        print(f"Error navigating to {contact_url}: {e}")
                        continue

            page_content = await page.content()
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', page_content)

            if emails:
                print(colored(f"Found emails: {emails}", "green"))
                all_emails.extend(emails)
            else:
                print(colored("No emails found on this page.", "red"))
        except Exception as e:
            print(f"Error occurred while scraping {url}: {e}")
        finally:
            await page.close()

    await browser.close()
    return list(set(all_emails))

def read_urls_from_file(file_path):
    """Reads URLs from a file."""
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            urls = [line.strip() for line in file.readlines() if line.strip()]
        return urls
    else:
        print(colored(f"File not found: {file_path}", "red"))
        return []

def save_emails_to_file(emails):
    """Saves collected emails to a text file."""
    output_file_path = os.path.expanduser("~/Desktop/collected_emails.txt")
    with open(output_file_path, "w") as file:
        for email in emails:
            file.write(f"{email}\n")
    print(colored(f"Emails saved to {output_file_path}", "cyan"))

def main():
    print_banner()

    # Input file path with more professional phrasing
    file_path = input(colored("Please enter the file path containing the URLs:\n", "magenta"))

    # Read URLs from the file
    urls = read_urls_from_file(file_path)

    if urls:
        emails = asyncio.run(scrape_emails_with_pyppeteer(urls))
        if emails:
            print(colored("\nCollected Emails:", "yellow"))
            for email in emails:
                print(colored(email, "green"))
            # Save emails to file
            save_emails_to_file(emails)
        else:
            print(colored("\nNo emails found.", "red"))
    else:
        print(colored("No URLs found in the file. Please provide a valid file.", "red"))

if __name__ == "__main__":
    main()
