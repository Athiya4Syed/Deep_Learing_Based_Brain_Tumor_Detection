# Medical Chatbot Setup Instructions

## Overview
The brain tumor detection application now includes a medical AI chatbot powered by Google's Gemini AI. The chatbot can answer questions about brain tumors, symptoms, treatments, and general medical concerns.

## Features Added

### 1. Medical Chatbot
- **AI-Powered**: Uses Google Gemini AI for intelligent medical responses
- **Context-Aware**: Can use recent scan results to provide personalized advice
- **Medical Knowledge**: Specialized in brain tumor detection and neurological conditions
- **Interactive UI**: Modern chat interface with typing indicators and suggestions
- **Persistent**: Maintains conversation history during the session

### 2. Enhanced Button Styles
- **Modern Design**: Sleek buttons with hover effects and animations
- **Multiple Variants**: Primary, secondary, and outline button styles
- **Responsive**: Works well on all device sizes
- **Accessible**: Proper focus states and keyboard navigation

### 3. Light Theme Support
- **Complete Theme System**: Light and dark themes across all pages
- **Persistent Preferences**: Theme choice is saved in browser localStorage
- **Smooth Transitions**: Animated theme switching
- **Consistent Design**: All pages support both themes

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Gemini AI API Key

#### Option A: Environment Variable (Recommended)
```bash
# Set the environment variable
export GEMINI_API_KEY="your-actual-api-key-here"

# Or on Windows
set GEMINI_API_KEY=your-actual-api-key-here
```

#### Option B: Direct Configuration
Edit `chatbot_service.py` and replace:
```python
api_key = "your-gemini-api-key-here"  # Replace with actual key
```

### 3. Get Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key and use it in your configuration

### 4. Run the Application
```bash
python main.py
```

## Usage

### Chatbot Features
1. **Click the chat icon** in the bottom-right corner to open the chatbot
2. **Ask medical questions** about brain tumors, symptoms, or treatments
3. **Use suggested questions** for quick access to common topics
4. **Context-aware responses** when you have recent scan results

### Theme Toggle
1. **Click the theme toggle** in the header to switch between light and dark themes
2. **Automatic persistence** - your choice is remembered across sessions
3. **Consistent across pages** - theme applies to all application pages

### Enhanced Buttons
- **Start Analysis**: Scrolls to upload section
- **New Patient**: Goes to patient information form
- **View Reports**: Shows all generated reports

## API Endpoints

### Chatbot Endpoints
- `POST /chatbot/message` - Send a message to the chatbot
- `GET /chatbot/suggestions` - Get suggested questions
- `POST /chatbot/clear` - Clear conversation history

### Example Usage
```javascript
// Send a message to the chatbot
fetch('/chatbot/message', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        message: 'What are the symptoms of brain tumors?',
        context: {
            recent_scan: 'Glioma',
            confidence: 85
        }
    })
})
.then(response => response.json())
.then(data => console.log(data.response));
```

## Troubleshooting

### Chatbot Not Working
1. **Check API Key**: Ensure GEMINI_API_KEY is set correctly
2. **Check Internet**: Gemini AI requires internet connection
3. **Check Console**: Look for JavaScript errors in browser console
4. **Check Server Logs**: Look for Python errors in terminal

### Theme Not Persisting
1. **Check localStorage**: Ensure browser allows localStorage
2. **Check JavaScript**: Ensure no JavaScript errors are blocking theme functions
3. **Clear Browser Cache**: Try clearing browser cache and cookies

### Buttons Not Styled
1. **Check CSS**: Ensure all CSS is loading properly
2. **Check Classes**: Ensure buttons have correct CSS classes
3. **Check Browser**: Ensure browser supports modern CSS features

## Security Notes

1. **API Key Security**: Never commit your actual API key to version control
2. **Environment Variables**: Use environment variables for production
3. **Rate Limiting**: Consider implementing rate limiting for chatbot requests
4. **Input Validation**: The chatbot validates all user inputs

## Future Enhancements

- [ ] Voice input/output for chatbot
- [ ] Multi-language support
- [ ] Advanced medical image analysis integration
- [ ] Doctor-patient chat history
- [ ] Export chat conversations
- [ ] Advanced theme customization options

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the application logs
3. Ensure all dependencies are installed correctly
4. Verify your Gemini API key is valid and has proper permissions

