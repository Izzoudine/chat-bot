import google.generativeai as genai
import os

API_KEY = "AIzaSyCxL5Y20IrZmjKo4cKKT5jkeYzjetoOUPk" # Trying the first key
genai.configure(api_key=API_KEY)

print("Listing available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error listing models: {e}")
