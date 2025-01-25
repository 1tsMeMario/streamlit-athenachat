import os
from pathlib import Path

# Path Configuration
BASE_DIR = Path(__file__).parent
PERSONAS_PATH = BASE_DIR / "personas/all.json"
CONVERSATIONS_DIR = BASE_DIR / "data"
CONVERSATIONS_FILE = CONVERSATIONS_DIR / "conversations.json"

# Ensure directories exist
CONVERSATIONS_DIR.mkdir(parents=True, exist_ok=True)

# Model Configuration
DEFAULT_MODEL = "darkidol-llama-3.1-8b-instruct-1.2-uncensored"
AVAILABLE_MODELS = ["darkidol-llama-3.1-8b-instruct-1.2-uncensored", "hermes-3-llama-3.2-3b", "llama-3-8b-lexi-uncensored"]

BOT_AVATAR = "https://files.catbox.moe/x3kr0e.png"
USER_AVATAR = "https://files.catbox.moe/u2y7vf.jpg"
