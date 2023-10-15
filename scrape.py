# This is a web scraping tool. This python file scrapes the GVSU ACI webpages and stores the scraped text in the Laker Mobile firebase database.

import os
import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


# Initialize Firebase with your service account key
cred = credentials.Certificate("ADD-FIREBASE-CREDENTIAL-JSON-FILE")
firebase_admin.initialize_app(cred)

# Get a reference to your Firestore database
db = firestore.client()

# Function to scrape all text and links from a given URL
def scrape_all_text_and_links_from_url(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract text between <p> tags and href from <a> tags
            paragraphs_and_links = []

            # Extract text between <p> tags
            paragraphs = soup.find_all('p')
            for paragraph in paragraphs:
                paragraphs_and_links.append({
                    "type": "p",
                    "text": paragraph.get_text()
                })

            # Extract href and text from <a> tags
            anchor_links = soup.find_all('a', href=True)
            for anchor_link in anchor_links:
                paragraphs_and_links.append({
                    "type": "a",
                    "href": anchor_link['href'],
                    "text": anchor_link.get_text()
                })

            # Create a document for each paragraph and anchor data
            for idx, data in enumerate(paragraphs_and_links):
                data["url"] = url

                # Add the data to Firestore with a specific document ID
                doc_ref = db.collection("paragraphs").document(f"{url.replace('/', '_')}_{idx}")
                doc_ref.set(data)

                print(f"Data from {url} added to Firestore with document ID: {doc_ref.id}")

            return '\n'.join(paragraphs_and_links)
        else:
            print(f"Failed to retrieve content from {url}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while scraping {url}: {str(e)}")
        return None

# List of URLs to scrape
urls_to_scrape = [
    'https://www.gvsu.edu/aci/',
    'https://www.gvsu.edu/aci/application-research-22.htm',
    'https://www.gvsu.edu/aci/ai-machine-learning-23.htm',
    'https://www.gvsu.edu/aci/bioinformatics-high-performance-computing-25.htm',
    'https://www.gvsu.edu/aci/applied-computing-services-laboratory-5.htm',
    'https://www.gvsu.edu/aci/sponsored-senior-projects-4.htm',
    'https://www.gvsu.edu/aci/give-to-aci-18.htm',
    'https://www.gvsu.edu/aci/student-opportunities-6.htm',
    'https://www.gvsu.edu/aci/computer-science-senior-projects-16.htm',
    'https://www.gvsu.edu/aci/research-dissemination-grant-19.htm',
    'https://www.gvsu.edu/aci/the-aci-residency-program-17.htm',
    'https://www.gvsu.edu/aci/aci-blog-7.htm',
    'https://www.gvsu.edu/aci/module-news-view.htm?storyId=4271D4CE-ADE6-6B2F-F4BA7E24DD2CCBD9&siteModuleId=0324BEDD-08D2-9A14-7FA65E12895C55DE',
    'https://www.gvsu.edu/aci/module-news-view.htm?storyId=D2E467CD-9F0B-7EC1-311DADE66EFC581B&siteModuleId=0324BEDD-08D2-9A14-7FA65E12895C55DE',
    'https://www.gvsu.edu/aci/module-news-view.htm?storyId=E5B1E817-0567-C9E8-7ACA61D7554166EB&siteModuleId=0324BEDD-08D2-9A14-7FA65E12895C55DE',
    'https://www.gvsu.edu/aci/module-news-view.htm?storyId=AC4469F6-D934-3BFD-0439A044EA8C6100&siteModuleId=0324BEDD-08D2-9A14-7FA65E12895C55DE',
    'https://www.gvsu.edu/aci/module-news-view.htm?storyId=D6678738-DBA6-0176-D4E96931C3E05A5C&siteModuleId=0324BEDD-08D2-9A14-7FA65E12895C55DE',
    'https://www.gvsu.edu/aci/about-aci-21.htm',
    # Add more URLs here
]

# Create a directory to store the output files if it doesn't exist
output_directory = 'scraped_data'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Loop through the list of URLs and scrape text and links
for url in urls_to_scrape:
    scraped_text = scrape_all_text_and_links_from_url(url)
    if scraped_text:
        # Create a separate text file for each URL
        file_name = os.path.join(output_directory, f"{url.split('//')[1].replace('/', '_')}.txt")
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(scraped_text)

print("Scraped data has been saved in separate text files with spaces trimmed.")
