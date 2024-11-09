import re
import requests
import requests.exceptions
from urllib.parse import urlsplit
from bs4 import BeautifulSoup

def get_emails(starting_url, max_emails=5):
    # a queue of urls to be crawled
    unprocessed_urls = [starting_url]
    
    # set of already crawled urls
    processed_urls = set()
    
    # list of fetched emails
    emails = []

    while unprocessed_urls and len(emails) < max_emails:
        # move next url from the list to the set of processed urls
        url = unprocessed_urls.pop(0)
        processed_urls.add(url)

        # extract base url to resolve relative links
        parts = urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        path = url[:url.rfind('/')+1] if '/' in parts.path else url

        # get url's content
        print(f"Crawling URL {url}")
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue

        # Update the email regex pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        # extract email addresses
        new_emails = re.findall(email_pattern, response.text, re.I)
        # Filter out image filenames
        new_emails = [email for email in new_emails if not email.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        emails.extend(new_emails)
        emails = list(dict.fromkeys(emails))  # remove duplicates while preserving order
        emails = emails[:max_emails]  # limit to max_emails

        if len(emails) >= max_emails:
            break

        # parse the HTML and find new links
        soup = BeautifulSoup(response.text, 'lxml')
        for anchor in soup.find_all("a"):
            link = anchor.attrs.get("href", '')
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            if link not in unprocessed_urls and link not in processed_urls:
                unprocessed_urls.append(link)

    return emails

# Example usage:
starting_url = 'https://www.raisingcanes.com/home/'
result = get_emails(starting_url)
print(result)