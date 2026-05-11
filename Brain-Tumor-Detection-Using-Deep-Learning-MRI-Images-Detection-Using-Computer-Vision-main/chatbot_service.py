import requests
import os
import json
from typing import Dict, List, Optional

class MedicalChatbot:
    def __init__(self):
        """Initialize the medical chatbot with Gemini AI via REST API"""
        # Set up Gemini API key
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key or self.api_key == 'your-gemini-api-key-here':
            # Use the provided API key as fallback
            self.api_key = "AIzaSyAnn3riwKa-w_mSemMja0nVbgM0ui5vWh8"
            print("✅ Using configured Gemini API key for chatbot functionality")
        
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        
        # Medical knowledge base for context
        self.medical_context = """
        You are a medical AI assistant specializing in brain tumor detection and neurological conditions. 
        You have access to information about:
        
        1. Brain Tumor Types:
           - Pituitary tumors: Usually benign, affect hormone production
           - Gliomas: Can be benign or malignant, arise from glial cells
           - Meningiomas: Usually benign, form on brain membranes
           - No tumor: Normal brain tissue
        
        2. Common Symptoms:
           - Headaches, seizures, vision problems
           - Memory issues, personality changes
           - Weakness, coordination problems
        
        3. Treatment Options:
           - Surgery, radiation therapy, chemotherapy
           - Medication, monitoring, lifestyle changes
        
        4. Important Disclaimers:
           - Always recommend consulting healthcare professionals
           - This is for informational purposes only
           - Not a substitute for medical diagnosis or treatment
        
        Provide helpful, accurate, and empathetic responses while always emphasizing the need for professional medical consultation.
        """
        
        # Conversation history for context
        self.conversation_history = []
    
    def get_response(self, user_message: str, user_context: Optional[Dict] = None) -> Dict:
        """
        Get a response from the medical chatbot
        
        Args:
            user_message: The user's question or message
            user_context: Optional context about the user (e.g., recent scan results)
        
        Returns:
            Dict containing the response and metadata
        """
        try:
            # Build the prompt with context
            full_prompt = self._build_prompt(user_message, user_context)
            
            # Prepare request payload
            payload = {
                "contents": [{
                    "parts": [{"text": full_prompt}]
                }]
            }
            
            headers = {
                'Content-Type': 'application/json'
            }
            
            # Make API call
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "error": f"API Error: {response.status_code} - {response.text}",
                    "response": "I apologize, but I'm experiencing technical difficulties. Please try again later.",
                    "timestamp": self._get_timestamp()
                }
            
            response_data = response.json()
            
            # Extract text from response
            try:
                candidates = response_data.get('candidates', [])
                if candidates and candidates[0].get('content') and candidates[0]['content'].get('parts'):
                    response_text = candidates[0]['content']['parts'][0]['text']
                else:
                    response_text = "I apologize, but I couldn't generate a response."
            except Exception as e:
                response_text = f"Error parsing response: {str(e)}"
            
            # Store conversation for context
            self.conversation_history.append({
                "user": user_message,
                "assistant": response_text,
                "timestamp": self._get_timestamp()
            })
            
            # Keep only last 10 exchanges to manage context length
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return {
                "success": True,
                "response": response_text,
                "timestamp": self._get_timestamp(),
                "context_used": user_context is not None
            }
            
        except Exception as e:
            print(f"Chatbot error: {str(e)}")  # Debug logging
            return {
                "success": False,
                "error": str(e),
                "response": "I apologize, but I'm experiencing technical difficulties. Please try again later or consult with a healthcare professional for immediate medical concerns.",
                "timestamp": self._get_timestamp()
            }
    
    def _build_prompt(self, user_message: str, user_context: Optional[Dict] = None) -> str:
        """Build the complete prompt for the AI model"""
        prompt_parts = [self.medical_context]
        
        # Add user context if available
        if user_context:
            context_str = self._format_user_context(user_context)
            prompt_parts.append(f"User Context: {context_str}")
        
        # Add recent conversation history
        if self.conversation_history:
            history_str = self._format_conversation_history()
            prompt_parts.append(f"Recent Conversation:\n{history_str}")
        
        # Add the current user message
        prompt_parts.append(f"User Question: {user_message}")
        
        # Add instructions
        prompt_parts.append("""
        Please provide a helpful, accurate, and empathetic response. Remember to:
        1. Be clear and easy to understand
        2. Always recommend consulting healthcare professionals for medical decisions
        3. Provide relevant information based on the context
        4. Be supportive and reassuring
        5. Include appropriate disclaimers
        """)
        
        return "\n\n".join(prompt_parts)
    
    def _format_user_context(self, context: Dict) -> str:
        """Format user context for the prompt"""
        context_parts = []
        
        if context.get('recent_scan'):
            context_parts.append(f"Recent scan result: {context['recent_scan']}")
        
        if context.get('tumor_type'):
            context_parts.append(f"Detected tumor type: {context['tumor_type']}")
        
        if context.get('stage'):
            context_parts.append(f"Tumor stage: {context['stage']}")
        
        if context.get('confidence'):
            context_parts.append(f"Detection confidence: {context['confidence']}%")
        
        if context.get('symptoms'):
            context_parts.append(f"Reported symptoms: {', '.join(context['symptoms'])}")
        
        return "; ".join(context_parts) if context_parts else "No specific context provided"
    
    def _format_conversation_history(self) -> str:
        """Format conversation history for context"""
        history_lines = []
        for exchange in self.conversation_history[-5:]:  # Last 5 exchanges
            history_lines.append(f"User: {exchange['user']}")
            history_lines.append(f"Assistant: {exchange['assistant']}")
            history_lines.append("---")
        
        return "\n".join(history_lines)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def get_suggested_questions(self) -> List[str]:
        """Get a list of suggested questions for users"""
        return [
            "What are the common symptoms of brain tumors?",
            "How are brain tumors typically treated?",
            "What should I do if I have persistent headaches?",
            "What is the difference between benign and malignant brain tumors?",
            "How often should I get brain scans?",
            "What lifestyle changes can help with brain health?",
            "What are the side effects of brain tumor treatments?",
            "How can I support someone with a brain tumor diagnosis?",
            "What questions should I ask my doctor about brain tumors?",
            "Are there any new treatments for brain tumors?"
        ]
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []

# Initialize the chatbot instance
medical_chatbot = MedicalChatbot()
