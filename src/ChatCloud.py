from wordcloud import WordCloud
import re


class ChatCloud:
    @staticmethod
    def extract_data(json_data: dict) -> list[str]:
        keys = ['media_type', 'forwarded_from']
        messages_dicts = []

        for message in json_data['messages']:
            if all(k not in message for k in keys) and message['text']:
                messages_dicts.append(message)

        messages = []
        for message in messages_dicts:
            if not isinstance(message['text'], list):
                messages.append(message['text'])

        return messages

    @staticmethod
    def filter_data(messages: list[str]) -> str:
        words = ''
        with open('data/stopwords.txt', encoding='utf-8') as stop_words:
            stopwords = stop_words.read().split('\n')
        stopwords.extend(['это', 'ща', 'еще', 'просто', 'почему', 'не', 'ну', 'на', 'да', 'че'])

        for txt in messages:
            tokens = txt.lower().split()
            preproc_tokens = []
            for token in tokens:
                token = re.sub('ё', 'е', token)
                token = re.sub('[^a-zA-Zа-яА-Я]', '', token)
                if set(token) != {'х', 'а'} and token not in stopwords:
                    preproc_tokens.append(token)
            preproc_tokens = ' '.join(preproc_tokens)
            words += preproc_tokens + ' '
        words = words.strip()

        return words

    @staticmethod
    def create_cloud(words: str):
        word_cloud = WordCloud(width=1600,
                               height=1000,
                               random_state=42,
                               background_color='black',
                               collocation_threshold=12,
                               min_font_size=10).generate(words)

        return word_cloud.to_image()

    def handle(self, json_data):
        data = self.extract_data(json_data)
        filtered_data = self.filter_data(data)
        cloud_img = self.create_cloud(filtered_data)

        return cloud_img
