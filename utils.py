# utils.py

def access_nested_map(nested_map, path):
    """Access a nested map using a tuple path."""
    current = nested_map
    for key in path:
        current = current[key]  # raises KeyError if key not found
    return current
