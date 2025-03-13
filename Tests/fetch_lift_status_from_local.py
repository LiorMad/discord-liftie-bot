import json
from bs4 import BeautifulSoup

# Path to your local HTML file
file_path = 'liftie.html'

# Path to the output JSON file
output_file_path = '../lifts_status.json'

# Open and read the HTML content from the file
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Create a dictionary to store the resort data
resorts_data = []

# Find all section elements that contain resort data
sections = soup.find_all('section', class_='panel resort')

# Iterate over each section (resort) to extract lifts and their statuses
for section in sections:
    # Extract the resort name from the 'data-resort' attribute
    resort_name = section.get('data-resort', 'Unknown Resort')

    # Find all lift items within this section
    lifts = []
    for lift in section.find_all('li', class_='lift'):
        lift_name = lift.find('span', class_='name').text
        lift_status = lift.find('span', class_='status').get('class')[1]  # Get the second class (status)

        # Mapping status class to readable status
        if lift_status == 'ls-open':
            status = 'Open'
        elif lift_status == 'ls-closed':
            status = 'Closed'
        elif lift_status == 'ls-scheduled':
            status = 'Scheduled'
        elif lift_status == 'ls-hold':
            status = 'Hold'
        else:
            status = 'Unknown'

        # Append lift information to the lifts list
        lifts.append({"name": lift_name, "status": status})

    # Append the resort's data to the resorts_data list
    resorts_data.append({"resort": resort_name, "lifts": lifts})

# Write the result to a JSON file
with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(resorts_data, json_file, indent=4)

print(f"Lift data has been successfully saved to {output_file_path}")
