import requests
import os

BASE_URL = "http://localhost:5001"

def test_health():
    print("Testing Health Check...")
    try:
        res = requests.get(f"{BASE_URL}/health")
        print(f"Status: {res.status_code}")
        print(f"Response: {res.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")

def test_chat_text():
    print("\nTesting Chat (Text Only)...")
    try:
        res = requests.post(f"{BASE_URL}/chat", data={"message": "Quelle est l'architecture ?"}, stream=True)
        print("Response Stream:")
        for chunk in res.iter_content(chunk_size=1024):
            print(chunk.decode('utf-8'), end="")
        print()
    except Exception as e:
        print(f"Chat text failed: {e}")

def test_csv_upload():
    print("\nTesting CSV Upload...")
    # Create dummy csv if not exists
    if not os.path.exists("small_test.csv"):
        with open("small_test.csv", "w") as f:
            f.write("transferId,payerId,payeeId,amount,currency,scenario\n1,27710000001,27710000002,100,USD,SUCCESS")
            
    try:
        with open("small_test.csv", "rb") as f:
            files = {'file': f}
            res = requests.post(f"{BASE_URL}/upload-csv", files=files)
            
        if res.status_code == 200:
            print("Success! Received ZIP file.")
            with open("test_report.zip", "wb") as f:
                f.write(res.content)
            print("Saved to test_report.zip")
        else:
            print(f"Error: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"CSV upload failed: {e}")

if __name__ == "__main__":
    test_health()
    test_chat_text()
    test_csv_upload()
