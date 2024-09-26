import os
from openai import OpenAI

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get your OpenAI API key from the environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

if openai_api_key is None:
    raise ValueError("No API key found in environment variables. Please check your .env file.")

# Set the OpenAI API key

# Fetch the list of models available to your account
models = client.models.list()

# Print the list of model names
for model in models.data:
    print(model)
