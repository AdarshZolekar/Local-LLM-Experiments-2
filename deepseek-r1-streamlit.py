from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import streamlit as st

# Initialize the ChatOllama model
chat = ChatOllama(model="deepseek-r1:1.5b")

# Set up Streamlit page
st.title("Deepseek R1 1.5B Assistant")
st.subheader("Tiny but mighty! 🚀 Powered by Ollama")
# st.subheader("Your personal AI companion running locally")

# Display welcome message in chat format
with st.chat_message("assistant"):
    st.write("Ask me anything!")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="You are a helpful AI assistant.")
    ]

# Display chat history
for message in st.session_state.messages[1:]:  # Skip the system message
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)
    else:
        with st.chat_message("assistant"):
            content = message.content
            if "<think>" in content and "</think>" in content:
                # Extract thinking content
                think_start = content.index("<think>")
                think_end = content.index("</think>") + len("</think>")
                thinking = content[think_start:think_end]
                actual_response = content[think_end:].strip()
                
                # Display thinking in expandable section
                with st.expander("Show AI thinking process"):
                    st.write(thinking)
                
                # Display actual response
                st.write(actual_response)
            else:
                st.write(content)

# Chat input
if prompt := st.chat_input("What's on your mind?"):
    # Add user message to chat history
    st.session_state.messages.append(HumanMessage(content=prompt))
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        thinking_placeholder = st.empty()  # Place thinking placeholder first
        message_placeholder = st.empty()   # Then message placeholder
        full_response = ""
        
        # Stream the response
        for chunk in chat.stream(st.session_state.messages):
            if chunk.content:
                full_response += chunk.content
                # Only update message placeholder during streaming if no thinking tags detected yet
                if "<think>" not in full_response:
                    message_placeholder.write(full_response)
        
        # After streaming is complete, check for thinking tags
        if "<think>" in full_response and "</think>" in full_response:
            # Extract thinking content
            think_start = full_response.index("<think>")
            think_end = full_response.index("</think>") + len("</think>")
            thinking = full_response[think_start:think_end]
            
            # Extract actual response
            actual_response = full_response[think_end:].strip()
            
            # First display thinking in expandable section
            with thinking_placeholder:
                with st.expander("Show AI thinking process"):
                    st.write(thinking)
            
            # Then display actual response
            message_placeholder.write(actual_response)
        else:
            # If no thinking tags, clear thinking placeholder and show full response
            thinking_placeholder.empty()
            message_placeholder.write(full_response)
    
    # Add AI response to chat history
    st.session_state.messages.append(AIMessage(content=full_response))

