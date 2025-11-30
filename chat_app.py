import streamlit as st
from google import genai
import os # अगर ज़रूरी हो तो

st.title("मेरा Buddy AI चैटबॉट 💬")

# 1. API Key और मॉडल की शुरुआत
if "GEMINI_API_KEY" not in st.secrets:
    st.error("कृपया Streamlit Secrets में GEMINI_API_KEY सेट करें।")
    # अगर Key नहीं है, तो चैट को निष्क्रिय रखें
    st.session_state.chat = None 
    st.session_state.messages = [{"role": "assistant", "content": "चैट शुरू करने के लिए API Key सेट करें।"}]
    
else:
    # API Key को सीधे GenerativeModel में पास करें (configure() को छोड़ दें)
    API_KEY = st.secrets["GEMINI_API_KEY"]
    model_name = "gemini-2.5-flash"
    
    if "chat" not in st.session_state:
        try:
            # Model को API Key के साथ initialize करें
            model = genai.GenerativeModel(model_name, api_key=API_KEY)
            st.session_state.chat = model.start_chat(history=[])
            st.session_state.messages = []
        except Exception as e:
            st.error(f"मॉडल शुरू करने में समस्या। क्या आपकी API Key सही है? Error: {e}")
            st.session_state.chat = None


# 2. पिछली चैट दिखाएँ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. यूज़र इनपुट लें और AI से जवाब प्राप्त करें
if prompt := st.chat_input("मैं आपकी कैसे मदद कर सकता हूँ?"):
    if st.session_state.chat is None:
        st.error("चैट API Key की कमी के कारण निष्क्रिय है।")
    
    else:
        # यूज़र का मैसेज दिखाएँ
        with st.chat_message("user"):
            st.markdown(prompt)

        # यूज़र के मैसेज को चैट हिस्ट्री में सेव करें
        st.session_state.messages.append({"role": "user", "content": prompt})

        # AI का जवाब प्राप्त करें 
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
