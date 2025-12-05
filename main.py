import sys
import json
import os
import requests
import google.generativeai as genai
from colorama import init, Fore, Style

# Initialize colorama
init()

# List of API keys to rotate through
API_KEYS = [
    "AIzaSyCxL5Y20IrZmjKo4cKKT5jkeYzjetoOUPk",
    "AIzaSyAVkj2Lfg7HonwghRZE7k0T2AGWZLADgkY",
    "AIzaSyB4tNZRZd1U6LRYtpFzFU8CLLABd7-OPTo"
]

def load_knowledge_base(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def upload_csv(file_path):
    url = "http://20.199.136.163:5000/transfer-bulk"
    print(f"{Fore.YELLOW}Uploading {file_path} to {url}...{Style.RESET_ALL}")
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files)

        if response.status_code == 200:
            output_filename = "rapport_resultat.zip"
            with open(output_filename, "wb") as f:
                f.write(response.content)
            return f"Success! Report downloaded as {output_filename}"
        else:
            return f"Error {response.status_code}: {response.text}"
    except FileNotFoundError:
        return f"Error: File not found at {file_path}"
    except Exception as e:
        return f"Error during upload: {str(e)}"

def get_model_response(user_input, knowledge_base_str):
    """
    Tries to get a response from the Gemini model using the available API keys.
    Rotates through keys if one fails.
    """
    system_prompt = f"""
    You are a helpful AI assistant for the 'Mojaloop Bulk Transfer Load Tester' project.
    Use the following technical documentation (Knowledge Base) to answer the user's questions accurately.
    
    KNOWLEDGE BASE:
    {knowledge_base_str}
    
    IMPORTANT:
    If the user wants to upload a CSV file or run a test with a file, instruct them to type:
    'upload <path_to_file.csv>'
    
    If the answer is not in the knowledge base, politely say you don't have that information.
    Keep answers concise and technical where appropriate.
    """

    for key in API_KEYS:
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel('gemini-2.5-pro')
            
            # Construct the full prompt
            full_prompt = f"{system_prompt}\n\nUser Question: {user_input}"
            
            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: API Key failed. Switching to next key... (Error: {e}){Style.RESET_ALL}")
            continue
    
    return "Error: All API keys failed. Please check your internet connection or API quotas."

def main():
    print(f"{Fore.CYAN}Welcome to the Mojaloop Load Tester Assistant! Type 'exit' to end.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}To upload a CSV file, type: upload <path_to_file>{Style.RESET_ALL}")
    
    kb_path = os.path.join(os.path.dirname(__file__), 'data', 'knowledge_base.json')
    knowledge_base = load_knowledge_base(kb_path)
    
    # Convert knowledge base to string for the prompt
    knowledge_base_str = json.dumps(knowledge_base, indent=2, ensure_ascii=False)
    
    while True:
        try:
            user_input = input(f"{Fore.GREEN}You: {Style.RESET_ALL}")
            if not user_input:
                continue
            
            if user_input.lower() in ["exit", "quit", "bye"]:
                print(f"{Fore.CYAN}Bot: Goodbye!{Style.RESET_ALL}")
                break
            
            # Check for upload command
            if user_input.lower().startswith("upload "):
                file_path = user_input[7:].strip().strip('"').strip("'")
                response = upload_csv(file_path)
                print(f"{Fore.CYAN}Bot: {response}{Style.RESET_ALL}")
                continue

            print(f"{Fore.YELLOW}Bot is thinking...{Style.RESET_ALL}", end="\r")
            response = get_model_response(user_input, knowledge_base_str)
            # Clear the "thinking" line
            print(" " * 50, end="\r")
            
            print(f"{Fore.CYAN}Bot: {response}{Style.RESET_ALL}")
            
        except KeyboardInterrupt:
            print(f"\n{Fore.CYAN}Bot: Goodbye!{Style.RESET_ALL}")
            break

if __name__ == "__main__":
    main()
