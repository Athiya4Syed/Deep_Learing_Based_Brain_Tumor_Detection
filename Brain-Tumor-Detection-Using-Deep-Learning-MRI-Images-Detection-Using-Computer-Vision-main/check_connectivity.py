import requests
import json
import os

def check_connectivity():
    print("🌐 Checking connectivity to Gemini API via REST...")
    
    api_key = "AIzaSyAnn3riwKa-w_mSemMja0nVbgM0ui5vWh8"
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    try:
        print(f"📡 Sending GET request to {url[:50]}...")
        response = requests.get(url, timeout=10)
        
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ REST API Connection Successful!")
            models = response.json().get('models', [])
            models = response.json().get('models', [])
            log_msg = f"Found {len(models)} models. Flash models:\n"
            for m in models:
                if 'flash' in m['name'].lower():
                    log_msg += f"- {m['name']}\n"
            print(log_msg)
            with open("connectivity.log", "w", encoding="utf-8") as f:
                f.write(log_msg)
        else:
            print(f"❌ REST API Connection Failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    check_connectivity()
