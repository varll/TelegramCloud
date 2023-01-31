from wordcloud import WordCloud, ImageColorGenerator
from datetime import datetime
from PIL import Image
import numpy as np
import re
import string


class ChatCloud:
    def __init__(self):
        self.messages = []
        self.dates = []

    def extract_data(self, json_data: dict):
        keys = ['media_type', 'forwarded_from']
        messages_dicts = []

        for message in json_data['messages']:
            if all(k not in message for k in keys) and message['text']:
                messages_dicts.append(message)

        for message in messages_dicts:
            if not isinstance(message['text'], list):
                self.messages.append(message['text'])
                self.dates.append(message['date'])

        self.dates = list(map(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S').date(), self.dates))

    def filter_data(self) -> list[str]:
        words = []
        with open('data/stopwords.txt', encoding='utf-8') as stop_words:
            stopwords = stop_words.read().split('\n')
        stopwords.extend(['это', 'ща', 'еще', 'просто', 'почему', 'не', 'ну', 'на', 'да', 'че'])

        emoji_re = r'\U0001F600-\U0001F64F' \
                   r'\U0001F300-\U0001F5FF' \
                   r'\U0001F680-\U0001F6FF' \
                   r'\U0001F1E0-\U0001F1FF'

        for txt in self.messages:
            tokens = txt.lower().split()
            preproc_tokens = []
            for token in tokens:
                token = re.sub('ё', 'е', token)
                token = re.sub('[^a-zA-Zа-яА-Я{emoji_re}]'.format(emoji_re=emoji_re), '', token)
                if set(token) != {'х', 'а'} and token not in stopwords:
                    preproc_tokens.append(token.strip())
            preproc_tokens = ' '.join(preproc_tokens)
            words.append(preproc_tokens)

        return words

    def get_dates_range(self):
        return min(self.dates), max(self.dates)

    def get_date_messages(self, words: list[str], start_date: datetime, end_date: datetime):
        start_idx = np.where([date >= start_date for date in self.dates])[0][0]
        end_idx = len(self.dates) - np.where([date <= end_date for date in self.dates[::-1]])[0][0] - 1

        date_messages = ' '.join(words[start_idx:end_idx])

        return date_messages

    @staticmethod
    def create_cloud(messages: str, img, emoji, background_color: str, colormap: str):
        params = {}

        image_colors = None
        if img:
            coloring = np.array(Image.open(img))
            params['mask'] = coloring
            image_colors = ImageColorGenerator(coloring)
        else:
            params['min_font_size'] = 12

        normal_word = r"(?:\w[\w']+)"
        emoji_re = r""
        if emoji:
            emoji_re = r"(?:[^\s])(?<![\w{ascii_printable}])".format(ascii_printable=string.printable)
        regexp = r"{normal_word}|{emoji}".format(normal_word=normal_word, emoji=emoji_re)
        params['regexp'] = regexp

        word_cloud = WordCloud(font_path='data/Symbola.ttf',
                               width=1920,
                               height=1080,
                               random_state=42,
                               background_color=background_color,
                               colormap=colormap.lower(),
                               collocation_threshold=12,
                               max_words=512,
                               **params).generate(messages)

        if image_colors:
            word_cloud = word_cloud.recolor(color_func=image_colors)

        return word_cloud.to_image()

    def handle(self, start_date: datetime, end_date: datetime, img, emoji, background_color: str, colormap: str):
        filtered_data = self.filter_data()
        date_messages = self.get_date_messages(filtered_data, start_date, end_date)
        cloud_img = self.create_cloud(date_messages, img, emoji, background_color, colormap)

        return cloud_img
