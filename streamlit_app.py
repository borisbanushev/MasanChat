import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

st.title("Masan Chatbot")

if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)