import streamlit as st
from datetime import datetime
import json

from src.ChatCloud import ChatCloud


class CloudApp:
    def __init__(self):
        self.chat_cloud = ChatCloud()
        self.start_date = datetime(2000, 5, 13).date()
        self.end_date = datetime(2027, 5, 13).date()

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

    @staticmethod
    def load_image():
        uploaded_file = st.file_uploader(
            label='Можно загрузить фото на белом фоне для маски',
            type=['png']
        )
        if uploaded_file is not None:
            return uploaded_file
        else:
            return None

    def run(self):
        st.title('Word Cloud')
        st.session_state.stage = 0

        chat = self.load_chat()
        if chat:
            self.chat_cloud.extract_data(chat)
            min_date, max_date = self.chat_cloud.get_dates_range()

            self.start_date = st.date_input('Дата начала', min_date, min_value=min_date, max_value=max_date)
            self.end_date = st.date_input('Дата конца', max_date, min_value=min_date, max_value=max_date)

            if self.start_date > self.end_date:
                st.error('Выберите нормальную дату')
            else:
                st.session_state.stage = 1

        if st.session_state.stage == 1:
            img = self.load_image()
            background_color = st.selectbox(
                'Цвет заднего фона',
                ('Black', 'White'))
            colormap = st.selectbox(
                'Цветовая карта',
                ('Viridis', 'Plasma', 'Inferno', 'Magma', 'Cividis'))
            emoji = st.checkbox('Оставить emoji')

            result = st.button('Построить облако')
            if result:
                cloud_img = self.chat_cloud.handle(
                    self.start_date,
                    self.end_date,
                    img,
                    emoji,
                    background_color,
                    colormap
                )
                st.image(cloud_img, use_column_width='always')


if __name__ == '__main__':
    cloud_app = CloudApp()
    cloud_app.run()


