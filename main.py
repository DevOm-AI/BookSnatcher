import requests
from bs4 import BeautifulSoup
import re
import os

def search_for_pdfs(query):
    print("Searching...")
    search_url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        pdf_urls = []
        for link in links:
            href = link['href']
            if re.search(r'\.pdf$', href):
                pdf_urls.append(href)
        return pdf_urls
    else:
        print("Failed to retrieve search results")
        return []

def download_pdf(pdf_url, download_folder):
    print("Downloading...")
    response = requests.get(pdf_url)
    if response.status_code == 200:
        pdf_filename = pdf_url.split('/')[-1]
        pdf_path = os.path.join(download_folder, pdf_filename)
        with open(pdf_path, 'wb') as f:
            f.write(response.content)
        print("Download Complete!")
    else:
        print(f"Failed to download PDF from: {pdf_url}")

def main(book_title, download_folder):
    query = f"{book_title} filetype:pdf"
    pdf_urls = search_for_pdfs(query)
    
    if pdf_urls:
        for pdf_url in pdf_urls:
            download_pdf(pdf_url, download_folder)
            return
    else:
        print("Book not found")

# Example usage
book_title = 'Rich Dad Poor Dad'  # Replace with the title of the book you're searching for
download_folder = 'D:\\Projects\\Web Book Scrapper\\Books'  # Replace with your desired download folder

# Create download folder if it does not exist
os.makedirs(download_folder, exist_ok=True)

main(book_title, download_folder)
