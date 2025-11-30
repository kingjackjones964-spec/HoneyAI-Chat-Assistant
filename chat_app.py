    # AI का जवाब प्राप्त करें (Streaming version)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""  # पूरा जवाब स्टोर करने के लिए एक खाली स्ट्रिंग
        
        try:
            # Gemini API से स्ट्रीमिंग जवाब प्राप्त करें
            response_stream = st.session_state.chat.send_message_streaming(prompt)
            
            for chunk in response_stream:
                # हर टुकड़े को जोड़ें और तुरंत स्क्रीन पर दिखाएँ
                if chunk.text:  # सुनिश्चित करें कि टेक्स्ट खाली न हो
                    full_response += chunk.text
                    # '▌' का उपयोग टाइपिंग इफ़ेक्ट दिखाने के लिए
                    message_placeholder.markdown(full_response + "▌") 
            
            # पूरा जवाब दिखाने के बाद टाइपिंग इफ़ेक्ट हटा दें
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            full_response = f"माफ़ करना, कनेक्शन में कोई समस्या है। Error: {e}"
            message_placeholder.markdown(full_response)

    # AI के जवाब को चैट हिस्ट्री में सेव करें
    st.session_state.messages.append({"role": "assistant", "content": full_response})
