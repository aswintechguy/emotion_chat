from openai import OpenAI
import streamlit as st
import os
import base64
import streamlit.components.v1 as components
import random

# set openai key
# os.environ["OPENAI_API_KEY"] = "your_openai_api_key"

# Set up the page configuration
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Function to encode a video file as base64
def get_video_base64(video_path):
    """Reads a video file and encodes it as a base64 string."""
    with open(video_path, "rb") as video_file:
        video_bytes = video_file.read()
    return base64.b64encode(video_bytes).decode("utf-8")

# Initialize session variables
if 'model' not in st.session_state:
    st.session_state['model'] = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant who can generate realistic responses about imaginary tokens. Do not use special characters like markdown and generate responses with appropriate emotion based on the query."}
    ]

if "default_video" not in st.session_state:
    st.session_state["default_video"] = get_video_base64("default.mp4")

if "new_video" not in st.session_state:
    st.session_state["new_video"] = None

if "is_new_video_playing" not in st.session_state:
    st.session_state["is_new_video_playing"] = False

if "emotion" not in st.session_state:
    st.session_state["emotion"] = None
    st.session_state['flag'] = 0

# Create columns for layout
col1, col2 = st.columns([0.20, 0.80])

# Column 1: Video
# Column 1: Video
with col1:
    # List of possible emotions
    labels = ["positive", "negative", "boring", "intriguing", "high_risk"]
    
    # Randomly select an emotion (ensure it's different from the current emotion)
    if st.session_state['flag'] == 0:
        st.session_state['flag'] = 1
    else:
        while True:
            emotion = random.choice(labels)
            if emotion != st.session_state["emotion"]:
                st.session_state["emotion"] = emotion
                break

    print("Current Emotion:", st.session_state["emotion"])

    # Set the video based on the selected emotion
    if st.session_state["emotion"] == 'positive':
        st.session_state["new_video"] = get_video_base64("emotions/happy.mp4")
        st.session_state["is_new_video_playing"] = True
    elif st.session_state["emotion"] == 'negative':
        st.session_state["new_video"] = get_video_base64("emotions/sad.mp4")
        st.session_state["is_new_video_playing"] = True
    elif st.session_state["emotion"] == 'boring':
        st.session_state["new_video"] = get_video_base64("emotions/sleepy.mp4")
        st.session_state["is_new_video_playing"] = True
    elif st.session_state["emotion"] == 'intriguing':
        st.session_state["new_video"] = get_video_base64("emotions/flirty.mp4")
        st.session_state["is_new_video_playing"] = True
    elif st.session_state["emotion"] == 'high_risk':
        st.session_state["new_video"] = get_video_base64("emotions/evil.mp4")
        st.session_state["is_new_video_playing"] = True

    # HTML for both default and overlay videos
    # Improved video player HTML with state management
    video_html = """
    <div style="position: relative; width: 100%; height: 240px;">
        <video 
            id="default-video" 
            autoplay 
            muted 
            loop 
            style="width: 100%; height: 100%; position: absolute; top: 0; left: 0;"
            playsinline>
            <source src="data:video/mp4;base64,{}" type="video/mp4">
        </video>

        <video 
            id="overlay-video" 
            muted 
            style="width: 100%; height: 100%; position: absolute; top: 0; left: 0; display: none;"
            playsinline>
            <source id="overlay-source" src="" type="video/mp4">
        </video>

        <script>
            // Store video state in localStorage
            const LOCAL_STORAGE_KEY = 'videoPlayerState';
            
            // Initialize or get stored state
            let storedState = localStorage.getItem(LOCAL_STORAGE_KEY);
            let playerState = storedState ? JSON.parse(storedState) : {{
                defaultVideoTime: 0,
                isOverlayPlaying: false
            }};

            const defaultVideo = document.getElementById('default-video');
            const overlayVideo = document.getElementById('overlay-video');
            const overlaySource = document.getElementById('overlay-source');
            
            // Restore default video state
            defaultVideo.addEventListener('loadedmetadata', () => {{
                defaultVideo.currentTime = playerState.defaultVideoTime;
            }});

            // Save video state periodically
            setInterval(() => {{
                if (defaultVideo) {{
                    playerState.defaultVideoTime = defaultVideo.currentTime;
                    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(playerState));
                }}
            }}, 1000);

            // Handle overlay video
            function playOverlayVideo() {{
                const newVideoBase64 = `{}`;
                if (!newVideoBase64) return;
                
                overlaySource.src = `data:video/mp4;base64,${{newVideoBase64}}`;
                overlayVideo.style.display = 'block';
                overlayVideo.load();
                
                overlayVideo.play().then(() => {{
                    playerState.isOverlayPlaying = true;
                    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(playerState));
                }});

                overlayVideo.onended = () => {{
                    overlayVideo.style.display = 'none';
                    overlaySource.src = '';
                    playerState.isOverlayPlaying = false;
                    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(playerState));
                }};
            }}

            // Check if we should play overlay video
            playOverlayVideo();
        </script>
    </div>
    """.format(
        st.session_state['default_video'],
        st.session_state['new_video'] or '',
        str(st.session_state['is_new_video_playing']).lower()
    )
    
    components.html(video_html, height=240)

# Column 2: Chat interface
with col2:
    st.title('Ask Glitches about tokens')
    messages_container = st.container(height=400)

    # Display previous messages
    for message in st.session_state['messages']:
        if message['role'] != 'system':
            with messages_container.chat_message(message['role']):
                st.markdown(message['content'])

    # Handle user input
    if prompt := st.chat_input("Enter your query"):
        st.session_state['messages'].append({"role": "user", "content": prompt})
        with messages_container.chat_message('user'):
            st.markdown(prompt)

        # add the emotion to the prompt appropriately
        messages_list = []
        for i, message in enumerate(st.session_state['messages']):
            if i == len(st.session_state['messages']) - 1:
                messages_list.append({"role": message["role"], "content": message["content"] + f". Give response with {st.session_state['emotion']} sentiment"})
            else:
                messages_list.append({"role": message["role"], "content": message["content"]})
        
        # Get response from the model
        
        with messages_container.chat_message('assistant', avatar='image.png'):
            client = st.session_state['model']
            stream = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=messages_list,
                temperature=0.8,
                max_tokens=1024,
                stream=True
            )

            response = st.write_stream(stream)
        # print(response)
        # Append the assistant's response to the messages
        st.session_state['messages'].append({"role": "assistant", "content": response})