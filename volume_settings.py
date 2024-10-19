import pygame

import os

VOLUME_FILE = "volume.txt"

def load_volume():
    """Load the volume level from a file."""
    if os.path.exists(VOLUME_FILE):
        with open(VOLUME_FILE, 'r') as file:
            try:
                return float(file.read().strip())
            except ValueError:
                return 0.5  # Default to 50% if there's an issue with reading
    return 0.5  # Default volume

def save_volume(volume):
    """Save the volume level to a file."""
    with open(VOLUME_FILE, 'w') as file:
        file.write(str(volume))


