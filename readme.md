# AI Chatbot with Emotion-Based Video Feedback

## Overview
This Streamlit application is an AI-powered chatbot that interacts with users and provides responses based on imaginary tokens. The chatbot dynamically changes the background video based on the emotion of the conversation (e.g., positive, negative, intriguing).

## Features
- **Chat Interface**: Interact with the chatbot using text queries.
- **Emotion-Based Video Feedback**: Background video changes based on the chatbot's emotional tone.
- **Dynamic Video Playback**: Default video with temporary overlay for emotions.
- **Streaming Responses**: Real-time responses from OpenAI's GPT model.

## How to Run
1. **Install Dependencies**:
   ```bash
   pip install streamlit openai
   ```

2. **Set OpenAI API Key**:
   Open emotion_chatbot.py, in line 9, uncomment and set the openai_api_key to use the model.

3. **Run the Application**:
   ```bash
   streamlit run emotion_chatbot.py
   ```

4. **Access the App**:
   - Open your browser and go to `http://localhost:8501`.

## File Structure
```
.
├── emotion_chatbot.py      # Main application file
├── default.mp4             # Default background video
├── emotions/               # Directory for emotion-based videos
│   ├── happy.mp4           # Positive emotion
│   ├── sad.mp4             # Negative emotion
│   ├── sleepy.mp4          # Boring emotion
│   ├── flirty.mp4          # Intriguing emotion
│   └── evil.mp4            # High-risk emotion
```

## Customization
- Replace video files in the `emotions` directory to customize feedback.
- Modify the system prompt in `st.session_state['messages']` to change chatbot behavior.