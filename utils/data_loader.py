import json
import os

# Get the parent directory of the current script
PARENT_DIR = os.path.dirname(os.path.abspath(__file__))  # Current directory
PARENT_DIR = os.path.dirname(PARENT_DIR)  # Parent directory

# Define the absolute path for the output JSON file
lifts_file = os.path.join(PARENT_DIR, 'data/lifts_status.json')

def load_resorts():
    """Load all resorts from the JSON file."""
    try:
        with open(lifts_file, "r") as file:
            resorts_data = json.load(file)
        return resorts_data
    except Exception as e:
        print(f"Error loading resorts data: {e}")
        return []