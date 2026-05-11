#!/usr/bin/env python3
"""
Test script for the medical chatbot functionality
"""

from chatbot_service import medical_chatbot

def test_chatbot():
    """Test the chatbot with sample medical questions"""
    
    print("🤖 Testing Medical Chatbot...")
    print("=" * 50)
    
    # Test questions
    test_questions = [
        "What are the symptoms of brain tumors?",
        "How are gliomas treated?",
        "What should I do if I have persistent headaches?",
        "What is the difference between benign and malignant brain tumors?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 Test {i}: {question}")
        print("-" * 40)
        
        response = medical_chatbot.get_response(question)
        
        if response["success"]:
            print(f"✅ Response: {response['response'][:200]}...")
        else:
            print(f"❌ Error: {response['error']}")
            print(f"Response: {response['response']}")
    
    print("\n" + "=" * 50)
    print("🎉 Chatbot testing completed!")

if __name__ == "__main__":
    test_chatbot()

