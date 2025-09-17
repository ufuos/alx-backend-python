import requests

def get_json(url):
    """Fetch JSON response from a given URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
