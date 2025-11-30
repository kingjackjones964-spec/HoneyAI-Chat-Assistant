import streamlit as st
from google import genai
import os

st.title("मेरा Buddy AI चैटबॉट 💬")

# 1. API Key कॉन्फ़िगरेशन (यह NameError/AttributeError को ठीक करता है)
# सुनिश्चित करें कि आपने Streamlit Secrets में GEMINI_API_KEY सेट किया हो
if "GEMINI_API_KEY" not in st.secrets:
    st.error("कृपया Streamlit Secrets में GEMINI_API_KEY सेट करें।")
else:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    except Exception as e:
        st.error(f"API Key कॉन्फ़िगरेशन में समस्या: {e}")

# 2. मॉडल और चैट की शुरुआत
# अगर 'chat' ऑब्जेक्ट सेशन स्टेट में नहीं है, तो नया चैट शुरू करें
if "chat" not in st.session_state:
    model_name = "gemini-2.5-flash"
    
    # यह सुनिश्चित करने के लिए कि genai कॉन्फ़िगर हो गया है
    if "GEMINI_API_KEY" in st.secrets:
        # अगर history मौजूद है तो उसका उपयोग करें, अन्यथा खाली लिस्ट
        st.session_state.chat = genai.GenerativeModel(model_name).start_chat(history=[])
        st.session_state.messages = []
    else:
        # अगर API key सेट नहीं है, तो चैट शुरू नहीं कर सकते
        st.session_state.chat = None
        st.session_state.messages = [{"role": "assistant", "content": "चैट शुरू करने के लिए API Key सेट करें।"}]


# 3. पिछली चैट दिखाएँ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. यूज़र इनपुट लें और AI से जवाब प्राप्त करें
if prompt := st.chat_input("मैं आपकी कैसे मदद कर सकता हूँ?"):
    if st.session_state.chat is None:
        st.error("चैट API Key की कमी के कारण निष्क्रिय है।")
    
    else:
        # यूज़र का मैसेज दिखाएँ
        with st.chat_message("user"):
            st.markdown(prompt)

        # यूज़र के मैसेज को चैट हिस्ट्री में सेव करें
        st.session_state.messages.append({"role": "user", "content": prompt})

        # AI का जवाब प्राप्त करें (Streaming version - यह IndentationError को ठीक करता है)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # Gemini API से स्ट्रीमिंग जवाब प्राप्त करें
                response_stream = st.session_state.chat.send_message_streaming(prompt)
                
                for chunk in response_stream:
                    if chunk.text:
                        full_response += chunk.text
                        message_placeholder.markdown(full_response + "▌") 
                
                # पूरा जवाब दिखाने के बाद टाइपिंग इफ़ेक्ट हटा दें
                message_placeholder.markdown(full_response)
                
            except Exception as e:
                full_response = f"माफ़ करना, कनेक्शन में कोई समस्या है। Error: {e}"
                message_placeholder.markdown(full_response)

        # AI के जवाब को चैट हिस्ट्री में सेव करें
        st.session_state.messages.append({"role": "assistant", "content": full_response})
