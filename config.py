

import os
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
MODEL_NAME = "Qwen/Qwen3-Coder-Next:novita"
BASE_URL = "https://router.huggingface.co/v1"

TEMPERATURE = 0.1 
MAX_TOKENS = 1500