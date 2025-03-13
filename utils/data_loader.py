import json

lifts_file = "../data/lifts_status.json"

def load_resorts():
    """Load all resorts from the JSON file."""
    try:
        with open(lifts_file, "r") as file:
            resorts_data = json.load(file)
        return resorts_data
    except Exception as e:
        print(f"Error loading resorts data: {e}")
        return []
