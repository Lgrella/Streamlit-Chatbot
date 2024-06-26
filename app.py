import streamlit as st
import openai

st.title("Chatbot with OpenAI")
st.write("This is a simple chatbot powered by OpenAI's GPT-3 model.")
st.write("You can ask it anything you want, and it will try to respond as best as it can.")


if "openai_model" not in st.session_state:
    st.session_state.openai_model = "gpt-3.5-turbo"

if "message" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What's Up?"):
    with st.chat_message("user", avatar="👩‍🎤"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
        ):
            if response.choices[0].finish_reason != "stop":
                full_response += response.choices[0].delta.content
            message_placeholder.markdown(full_response+ " ")
        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})