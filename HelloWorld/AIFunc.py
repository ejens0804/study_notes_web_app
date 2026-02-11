import sys
from google import genai #pip install google-genai
import time

#for text input only
def text_gemini(input=None):
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

#for text and file input WIP
#for local files uplodading; file argument should be filepath. To add extra file capacity, add file4, file5, etc
def upload_gemini(input=None, file1=None, file2=None, file3=None):
    api_key = "AIzaSyAioGahyYx-SIwZGDaKGz3EBRqEWovZFGs"
    client = genai.Client(api_key=api_key)
    contents = []
    if input:
        contents.append(input)
    for file in [file1, file2, file3]:
        if file:
            uploaded = client.files.upload(file=file)
            contents.append(uploaded)
    while True:
        try:
            response = client.models.generate_content(model="gemini-2.0-flash-lite",contents=contents)
            return response.text
        except Exception as e:
            if "503" in str(e) or "overloaded" in str(e):
                time.sleep(5)
            else:
                print(f"Unexpected error: {e}")
                sys.exit(e)



#alternate model arguments found at; https://ai.google.dev/gemini-api/docs/models
#attempt to use least advanced model to save cost

print(upload_gemini('string input', r"filepath(r ignores backslashes as escape characters) repeat as desired"))