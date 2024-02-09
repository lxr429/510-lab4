import requests
from bs4 import BeautifulSoup
import csv

def extract_event_urls(url):
    res = requests.get(url)
    
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')

        selector = "div.search-result-preview > div > h3 > a"
        a_eles = soup.select(selector)
        event_urls = [x['href'] for x in a_eles]
        return event_urls
    else:
        print(f"Failed to retrieve the page. Status code: {res.status_code}")
        return []

def scrape_event_urls(base_url):
    all_event_urls = []
    page_num = 1

    while True:
        page_url = f"{base_url}/page/{page_num}"
        event_urls = extract_event_urls(page_url)

        if not event_urls:
            break

        all_event_urls.extend(event_urls)
        page_num += 1

    return all_event_urls

def extract_event_details(event_url):
    res = requests.get(event_url)
    
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')

        
        name = soup.select('#body > div.global-wrapper > div.container-event-detail.padding-top-bottom > div:nth-child(1) > div.medium-6.columns.event-top > h1')[0].text
        date = soup.select('#body > div.global-wrapper > div.container-event-detail.padding-top-bottom > div:nth-child(1) > div.medium-6.columns.event-top > h4 > span:nth-child(1)')[0].text
        location = soup.select('#body > div.global-wrapper > div.container-event-detail.padding-top-bottom > div:nth-child(1) > div.medium-6.columns.event-top > h4 > span:nth-child(2)')[0].text
        event_type = soup.select('#body > div.global-wrapper > div.container-event-detail.padding-top-bottom > div:nth-child(1) > div.medium-6.columns.event-top > a:nth-child(3)')[0].text
        region = soup.select('#body > div.global-wrapper > div.container-event-detail.padding-top-bottom > div:nth-child(1) > div.medium-6.columns.event-top > a:nth-child(4)')[0].text

        return {'Name': name, 'Date': date, 'Location': location, 'Type': event_type, 'Region': region}
    else:
        print(f"Failed to retrieve the page. Status code: {res.status_code}")
        return None


def scrape_and_save_event_details(event_urls):
    event_details_list = []

    for event_url in event_urls:
        event_details = extract_event_details(event_url)

        if event_details:
            event_details_list.append(event_details)

    
    csv_file_path = 'events.csv'
    fields = ['Name', 'Date', 'Location', 'Type', 'Region']

    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(event_details_list)

    print(f"Event details have been saved to {csv_file_path}")


base_url = 'https://visitseattle.org/events'
event_urls = scrape_event_urls(base_url)


scrape_and_save_event_details(event_urls)