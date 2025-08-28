from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import streamlit as st
import os

# Set up Streamlit page
st.title("🚀 Deepseek-R1 Llama-70B Chat")
# st.write("⚡ Blazing-fast Thinking Model powered by Groq ❤️")
st.write("❤️ Built by [Build Fast with AI](https://buildfastwithai.com/genai-course)")

# Add sidebar for API key input and details
with st.sidebar:
    st.header("⚙️ Configuration")
    # Store API key directly in session state
    st.session_state.groq_api_key = st.text_input("GROQ API Key", type="password")
    
    # Add model details section
    st.divider()
    st.markdown("**Model Details**")
    st.caption("Running: `deepseek-r1-distill-llama-70b`")
    st.caption("Groq LPU Inference Engine")
    
    # Add New Chat button
    st.divider()
    if st.button("🔄 Start New Chat", use_container_width=True):
        st.session_state.messages = [
            SystemMessage(content="You are a helpful AI assistant.")
        ]
        st.rerun()
    
    # Add branding with hyperlink
    st.divider()
    st.markdown(
        "**Built by** [Build Fast with AI](https://buildfastwithai.com/genai-course)",
        unsafe_allow_html=True
    )

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
    # Check for API key in the input field directly
    if not st.session_state.groq_api_key:
        st.error("Please enter your GROQ API key in the sidebar")
        st.stop()
        
    # Initialize the ChatOpenAI model with Groq
    chat = ChatOpenAI(
        model="deepseek-r1-distill-llama-70b",
        openai_api_key=st.session_state.groq_api_key,
        openai_api_base="https://api.groq.com/openai/v1"
    )
    
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

