import re 
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit


def get_business_emails(business_list):
    """Get emails for each business."""
    print("retreiving emails")
    for business in business_list:
        if 'website' in business and business['website'] != '':
            
            business['email'] = extract_email_from_google(business['website'])
            print(business['email'])
    return business_list

def extract_email_from_google(website):
    """Extract email from a website."""
    # Remove http(s):// and path from the website URL
    domain = website.split('://', 1)[1].split('/', 1)[0]
    domain = domain.replace('www.', '')
    
    # Search for email on Google
    url = f'https://www.google.com/search?q="@{domain}" "email"'
    print(url)
    response = requests.get(url)
    emails = find_emails_in_text(response.content)
    return emails

def find_emails_in_text(html_content):
    """Find emails in HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    # print(soup)
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    emails = set(re.findall(email_pattern, soup.get_text()))
    new_emails = []
    for email in emails:
        # print(email)
        if not any(x in email.lower() for x in ['%22', 'john', 'jane', 'doe', 'first', 'last', 'smith']):
            new_emails.append(email)
    return new_emails

def extract_emails_from_website(starting_url, max_emails=1):
    """
    Extract emails from a website by crawling its pages.
    
    Args:
    starting_url (str): The URL to start crawling from.
    max_emails (int): Maximum number of emails to extract. Defaults to 1.
    
    Returns:
    list: A list of unique email addresses found on the website.
    """
    # a queue of urls to be crawled
    unprocessed_urls = [starting_url]
    
    # set of already crawled urls
    processed_urls = set()
    
    # list of fetched emails
    emails = []

    # Counter for processed links
    links_processed = 0

    while unprocessed_urls and len(emails) < max_emails and links_processed < 20:
        # move next url from the list to the set of processed urls
        url = unprocessed_urls.pop(0)
        processed_urls.add(url)
        links_processed += 1

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
