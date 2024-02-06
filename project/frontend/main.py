import streamlit as st

from backend_api import Novelist

novelist_client = Novelist("config.yaml")

st.title("NAMU-WIKI-LLM")

def init_session():
    if "message" not in st.session_state:
        st.session_state.message = []


def write_message(message):
    st.session_state.message.append(message)
    with st.chat_message(message["type"]):
        st.markdown(message["content"])


def main():

    for message in st.session_state.message:
        with st.chat_message(message["type"]):
            st.markdown(message["content"])

    if query := st.chat_input("Ask me"):
        message = {"type": "Question", "content": query}
        write_message(message)

        try:
            answer = novelist_client.get_response(query)    
        except:
            answer = "죄송합니다. 서버에 일시적 장애가 있습니다."
        
        message = {"type": "Answer", "content": answer}
        write_message(message)


if __name__ == "__main__":
    init_session()
    main()
