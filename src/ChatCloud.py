from wordcloud import WordCloud
# from nltk.corpus import stopwords

class ChatCloud:
    @staticmethod
    def filter_data(json_data: str) -> list[str]:
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
    def create_cloud(messages: list[str]):
        words = ''
        with open('data/stopwords.txt', encoding='utf8') as stopwords:
            stop_words = stopwords.read().split('\n')
        stop_words.extend(['это', 'ща', 'ещё', 'просто', 'почему'])

        for txt in messages:
            txt = str(txt)
            tokens = txt.lower().split()
            words += " ".join(tokens) + " "

        word_cloud = WordCloud(width=1600,
                               height=1000,
                               background_color='black',
                               stopwords=stop_words,
                               min_font_size=10).generate(words)

        return word_cloud.to_image()

    def handle(self, json_data):
        filtered_data = self.filter_data(json_data)
        cloud_img = self.create_cloud(filtered_data)

        return cloud_img
