from openai import OpenAI
import streamlit as st
import os
import base64
import streamlit.components.v1 as components

# give title to the page
st.title('AI Chatbot')

# Function to encode video file as base64
def get_video_base64(video_path):
    with open(video_path, "rb") as video_file:
        video_bytes = video_file.read()
    return base64.b64encode(video_bytes).decode("utf-8")

# initialize session variables at the start once
if 'model' not in st.session_state:
    st.session_state['model'] = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

if 'messages' not in st.session_state:
    st.session_state['messages'] = [ {"role": "system", "content": "You are a helpful assistant who can generate realistic response about the queries regarding tokens which user will ask. Use one of the following sentiments in the response style implicitly - Positive, Negative, Boring, Intriguing, High Risk."}]

if "default_video" not in st.session_state:
    st.session_state["default_video"] = get_video_base64("default.mp4")
if "new_video" not in st.session_state:
    st.session_state["new_video"] = None
if "is_new_video_playing" not in st.session_state:
    st.session_state["is_new_video_playing"] = False

# update the interface with the previous messages
for message in st.session_state['messages']:
    if message['role'] != 'system':
        with st.chat_message(message['role']):
            st.markdown(message['content'])

# create the chat interface
if prompt := st.chat_input("Enter your query"):
    st.session_state['messages'].append({"role": "user", "content": prompt})
    with st.chat_message('user'):
        st.markdown(prompt)

    # get response from the model
    with st.chat_message('assistant'):
        client = st.session_state['model']
        stream = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": message["role"], "content": message["content"]} for message in st.session_state['messages']
            ],
            temperature=0.8,
            max_tokens=1024,
            stream=True
        )

        response = st.write_stream(stream)
        emotion = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "user", "content": f"Context: {response}\nIdentify the sentiment for the above context from one of the following positive, negative, boring, intriguing, high_risk. If there are no sentiment or neutral return neutral. Output only the sentiment without additional text.\nSentiment: "}
            ],
            temperature=0.8,
            max_tokens=3
        )
        emotion = emotion.choices[0].message.content.lower()
        print(emotion)
        if emotion == 'positive':
            st.session_state["new_video"] = get_video_base64("emotions/happy.mp4")
            st.session_state["is_new_video_playing"] = True
        elif emotion == 'negative':
            st.session_state["new_video"] = get_video_base64("emotions/sad.mp4")
            st.session_state["is_new_video_playing"] = True
        elif emotion == 'boring':
            st.session_state["new_video"] = get_video_base64("emotions/sleepy.mp4")
            st.session_state["is_new_video_playing"] = True
        elif emotion == 'intriguing':
            st.session_state["new_video"] = get_video_base64("emotions/flirty.mp4")
            st.session_state["is_new_video_playing"] = True
        elif emotion == 'high_risk':
            st.session_state["new_video"] = get_video_base64("emotions/evil.mp4")
            st.session_state["is_new_video_playing"] = True
    st.session_state['messages'].append({"role": "assistant", "content": response})


# JavaScript for video playback logic
video_html = f"""
<div style="position: relative; width: 100%; height: 300px;">
    <!-- Default video (background) -->
    <video 
        id="default-video" 
        autoplay 
        muted 
        loop 
        style="width: 100%; height: 100%; position: absolute; top: 0; left: 0;">
        <source src="data:video/mp4;base64,{st.session_state['default_video']}" type="video/mp4">
    </video>

    <!-- Overlay video (for emotions) -->
    <video 
        id="overlay-video" 
        muted 
        style="width: 100%; height: 100%; position: absolute; top: 0; left: 0; display: none;">
        <source id="overlay-source" src="" type="video/mp4">
    </video>

    <script>
        const defaultVideo = document.getElementById('default-video');
        const overlayVideo = document.getElementById('overlay-video');
        const overlaySource = document.getElementById('overlay-source');
        let isNewVideoPlaying = {str(st.session_state['is_new_video_playing']).lower()};
        let newVideoBase64 = `{st.session_state['new_video'] or ''}`;

        function playOverlayVideo() {{
            if (!newVideoBase64) return;
            
            // Set up overlay video
            overlaySource.src = `data:video/mp4;base64,${{newVideoBase64}}`;
            overlayVideo.style.display = 'block';
            overlayVideo.load();
            overlayVideo.play();

            // When overlay video ends
            overlayVideo.onended = () => {{
                overlayVideo.style.display = 'none';
                overlaySource.src = '';
                isNewVideoPlaying = false;
            }};
        }}

        // Check if we should play new video
        if (isNewVideoPlaying && newVideoBase64) {{
            playOverlayVideo();
        }}
    </script>
</div>
"""

# Embed the video player in the sidebar
with st.sidebar:
    components.html(video_html, height=300)

# Reset the new video playing flag
if st.session_state.get("is_new_video_playing"):
    st.session_state["is_new_video_playing"] = False