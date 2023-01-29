import streamlit as st
import json

from src.ChatCloud import ChatCloud


class CloudApp:
    def __init__(self):
        self.chat_cloud = ChatCloud()

    @staticmethod
    def load_chat():
        uploaded_file = st.file_uploader(
            label='Загрузите json файл с дилогом',
            type=['json']
        )
        if uploaded_file is not None:
            json_chat = json.load(uploaded_file)
            return json_chat
        else:
            return None

    def run(self):
        st.title('Word Cloud')
        st.session_state.stage = 0

        chat = self.load_chat()
        if chat:
            st.session_state.stage = 1

        if st.session_state.stage == 1:
            result = st.button('Построить облако')
            if result:
                st.image(self.chat_cloud.handle(chat), use_column_width='always')


if __name__ == '__main__':
    cloud_app = CloudApp()
    cloud_app.run()


