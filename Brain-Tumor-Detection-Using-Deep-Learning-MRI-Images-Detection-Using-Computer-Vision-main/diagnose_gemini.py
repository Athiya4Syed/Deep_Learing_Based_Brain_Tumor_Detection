import google.generativeai as genai
import os
import sys

def diagnose():
    print("🔍 Starting Gemini Diagnostic...")
    
    # Hardcoded key from chatbot_service.py
    api_key = "AIzaSyAnn3riwKa-w_mSemMja0nVbgM0ui5vWh8"
    print(f"🔑 Using API Key: {api_key[:10]}...")
    
    try:
        genai.configure(api_key=api_key)
        print("✅ Configuration successful.")
    except Exception as e:
        print(f"❌ Configuration failed: {e}")
        return

    try:
        print("🤖 Initializing model...")
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("✅ Model initialized.")
        
        print("💬 Sending test message...")
        response = model.generate_content("Hello, are you working?")
        
        if response and response.text:
            print(f"✅ Response received: {response.text}")
        else:
            print("❌ Empty response received.")
            
    except Exception as e:
        print(f"❌ Error during generation: {e}")

if __name__ == "__main__":
    diagnose()
