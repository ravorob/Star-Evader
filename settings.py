import json

# Load settings from file
def load_settings():
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Default settings if file does not exist
        return {
            "volume": 0.8,
            "difficulty": "medium",
            "game_mode": "medium",
            "controls": {
                "left": "K_LEFT",
                "right": "K_RIGHT",
                "up": "K_UP",
                "down": "K_DOWN"
            }
        }

# Save settings to file
def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=4)
