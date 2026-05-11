import sys
import os
from chatbot_service import medical_chatbot

def log(message):
    print(message)
    with open("verification.log", "a", encoding="utf-8") as f:
        f.write(message + "\n")

def verify_chatbot():
    # Clear log file
    with open("verification.log", "w", encoding="utf-8") as f:
        f.write("")
        
    log("🤖 Verifying Medical Chatbot Tumor Questions...")
    log("=" * 60)
    
    test_cases = [
        {
            "question": "What is a glioma?",
            "keywords": ["glial", "brain", "tumor"],
            "description": "Definition of Glioma"
        },
        {
            "question": "Tell me about meningioma.",
            "keywords": ["meninges", "membranes", "brain"],
            "description": "Definition of Meningioma"
        },
        {
            "question": "What are the symptoms of a pituitary tumor?",
            "keywords": ["hormone", "vision", "headache"],
            "description": "Symptoms of Pituitary Tumor"
        }
    ]
    
    all_passed = True
    
    for i, test in enumerate(test_cases, 1):
        log(f"\n📝 Test {i}: {test['description']}")
        log(f"Question: {test['question']}")
        log("-" * 40)
        
        response_data = medical_chatbot.get_response(test['question'])
        
        if response_data["success"]:
            response_text = response_data["response"]
            log(f"✅ Response received: {response_text[:150]}...")
            
            # Check for keywords
            missing_keywords = [kw for kw in test['keywords'] if kw.lower() not in response_text.lower()]
            
            if not missing_keywords:
                log("✅ VERIFICATION: PASS - All keywords found.")
            else:
                log(f"⚠️ VERIFICATION: WARNING - Missing keywords: {missing_keywords}")
        else:
            log(f"❌ Error: {response_data['error']}")
            all_passed = False
            
    log("\n" + "=" * 60)
    if all_passed:
        log("🎉 All chatbot tests completed successfully.")
    else:
        log("❌ Some chatbot tests failed.")

if __name__ == "__main__":
    verify_chatbot()
