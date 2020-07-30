import pandas as pd
import requests
import datetime
from time import sleep
import re
from textblob import TextBlob
import numpy as np

class Thread:
    def __init__(self, permalink):
        self.comments=pd.DataFrame()
        self.ses = requests.session()
        self.ses.headers[
            'User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        self.extract_from_link(permalink)

    def extract_from_link(self, permalink):
        res = self.ses.get(f'https://api.reddit.com{permalink}')
        post, comments = res.json()
        self.__dict__.update(post['data']['children'][0]['data'])
        self.recur_comments(comments['data']['children'])

    def recur_comments(self, comments):
        self.comments = self.comments.append([c['data'] for c in comments],
                                             ignore_index=True)
        for c in comments:
            if c['data'].get('replies'):
                try:
                    self.recur_comments(
                        c['data']['replies']['data'].get('children'))
                except:
                    print(c['data']['replies']['data']['children']['data'])

    def sentiment(self, weighted=False):
        if 'sentiment' not in self.comments.columns:
            blobs = [TextBlob(str(text)) for text in self.comments.body]
            sent = np.array([blob.sentiment.polarity for blob in blobs])
            self.comments['sentiment'] = sent
        if weighted:
            scores = self.comments.score.fillna(0).astype('int32')
            return sum(self.comments.sentiment * scores) / sum(scores)
        return self.comments.sentiment