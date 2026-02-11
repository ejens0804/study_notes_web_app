import sys
from google import genai #pip install google-genai
import time

#allows text input only
def call_gemini(input):
    api_key = "AIzaSyAioGahyYx-SIwZGDaKGz3EBRqEWovZFGs"
    client = genai.Client(api_key=api_key)
    while True:
        try:
            response = client.models.generate_content(model='gemini-2.0-flash-lite', contents=input)
            return response.text
        except Exception as e:
            if "503" in str(e) or "overloaded" in str(e):
                time.sleep(5)
            else:
                print(f"An unexpected error has occured: {e}")
                sys.exit(e)

#alternate model arguments found at; https://ai.google.dev/gemini-api/docs/models
#attempt to use least advanced model to save cost