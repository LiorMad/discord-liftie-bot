import json
import requests
from bs4 import BeautifulSoup
import os

# URL to query data from
url = 'https://liftie.info/'

# Get the absolute path of the directory containing this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the absolute path for the output JSON file
output_file_path = os.path.join(BASE_DIR, 'lifts_status.json')

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Create a dictionary to store the resort data
    resorts_data = []

    # Find all section elements that contain resort data
    sections = soup.find_all('section', class_='panel resort')

    # Iterate over each section (resort) to extract lifts, statuses, and correct resort URLs
    for section in sections:
        # Extract the resort name from the 'data-resort' attribute
        resort_name = section.get('data-resort', 'Unknown Resort')

        # Extract the correct resort website URL (first <a> tag inside <header> with class="icon-alone resort-link")
        header = section.find('header')
        resort_url = None

        if header:
            resort_link_tag = header.find('a', class_='icon-alone resort-link')
            if resort_link_tag and 'href' in resort_link_tag.attrs:
                resort_url = resort_link_tag['href']

        # Find all lift items within this section
        lifts = []
        for lift in section.find_all('li', class_='lift'):
            lift_name = lift.find('span', class_='name').text
            lift_status = lift.find('span', class_='status').get('class')[1]  # Get the second class (status)

            # Mapping status class to readable status
            status_mapping = {
                'ls-open': 'Open',
                'ls-closed': 'Closed',
                'ls-scheduled': 'Scheduled',
                'ls-hold': 'Hold'
            }
            status = status_mapping.get(lift_status, 'Unknown')

            # Append lift information to the lifts list
            lifts.append({"name": lift_name, "status": status})

        # Append the resort's data to the resorts_data list
        resorts_data.append({"resort": resort_name, "url": resort_url, "lifts": lifts})

    # Write the result to a JSON file
    with open(output_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(resorts_data, json_file, indent=4)

    print(f"Lift data has been successfully saved to {output_file_path}")
else:
    print(f"Failed to retrieve data from {url}. HTTP Status code: {response.status_code}")
