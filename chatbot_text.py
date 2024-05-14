import streamlit as st
import openai

def ask_gpt(prompt, model, api_key):
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=prompt
        )
        gpt_response = response.choices[0].message.content
        return gpt_response
    except openai.error.OpenAIError as e:
        return f"Error: {e}"

with st.sidebar:
    st.session_state["OPENAI_API"]=st.text_input(label="OpenAI API키", placeholder="Enter your API key",value="",type="password")
    selected_model = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4"])

if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

col1,col2=st.columns([1,2])
with col1:
    st.subheader("질문하기")
    prompt=st.text_input("메시지를 입력하세요.")

with col2:
    for i in st.session_state.chat_log:
        with st.chat_message(i["role"]):
            st.markdown(i["content"])

    if prompt:
        with st.chat_message("user"):
            st.write(prompt)
            st.session_state.chat_log.append({"role": "user", "content": prompt})
        with st.spinner("Thinking..."):  # Loading indicator
            response = ask_gpt(st.session_state["chat_log"], selected_model, st.session_state["OPENAI_API"])
        with st.chat_message("ai"):
            st.write(response)
            st.session_state.chat_log.append({"role": "assistant", "content": response})

# Option to clear chat history (optional)
if st.button("Clear Chat History"):
    st.session_state.chat_log = []
