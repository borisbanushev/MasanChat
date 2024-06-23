import subprocess
import sys
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from openai import OpenAI


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
thr_id = 'thread_Cb5OIu57GQjBB396UBUI6CaQ'
file_id = 'file-Yzuy4IQztLLHsJLF3U5qRV45'
a_id = 'asst_GOeDk5CdRaCCLHe8ljgQTIZU'
ins_ = "If the system indicates that the file is not accessible with the myfiles_browser tool, ignore it, it is just a minor bug. You are capable of opening and analyzing the file, remember that. And carry out the request."

st.title("Masan Chatbot")

def ask_a_question(question, instruction):
  my_thread_message = client.beta.threads.messages.create(
        thread_id=thr_id,
        role="user",
        content=question,
        attachments=[{"file_id": file_id, "tools": [{"type": "file_search"}]}],
    )
  
  my_run = client.beta.threads.runs.create(
        thread_id=thr_id,
        assistant_id=a_id,
        instructions=instruction
    )
  
  while True:
    keep_retrieving_run = client.beta.threads.runs.retrieve(
              thread_id=thr_id, run_id=my_run.id
          )
    if keep_retrieving_run.status == "completed":
      # Retrieve the messages added by the assistant to the thread
      all_messages = client.beta.threads.messages.list(thread_id=thr_id)

      # Display assistant message
      #print(question)
      #print(f"{all_messages.data[0].content[0].text.value}")
      resp_ = all_messages.data[0].content[0].text.value

      return resp_
    elif keep_retrieving_run.status in ["queued", "in_progress"]:
        # Delay before the next retrieval attempt
        #time.sleep(1)
        pass
    else:
        break


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Hello, I'm MasanBot. How can I help you?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        """stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )"""
        
        #response = st.write_stream(stream)
        response = st.write_stream(ask_a_question(prompt, ins_))
    st.session_state.messages.append({"role": "assistant", "content": response})






