import os
import config
import openai
import logging

from utils import prettify
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    raise EnvironmentError('You should set OPENAI_API_KEY in your environment variable in .env file')


class NewsArticleGenerator:
    openai.api_key = OPENAI_API_KEY

    def __init__(self,
                 engine=config.ENGINE,
                 temperature=config.TEMPERATURE,
                 max_tokens=config.MAX_TOKENS,
                 top_p=config.TOP_P,
                 n=config.N,
                 frequency_penalty=config.FREQUENCY_PENALTY,
                 presence_penalty=config.PRESENCE_PENALTY):
        self.engine = engine
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.n = n
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty

    def generate_news_article(self, keywords: list):
        """
        :param keywords: list of keywords that we pass to the model to generate news articles
        :return: generated news article that went through content prettifier
        """
        try:
            model = openai.Completion.create(
                engine=self.engine,
                prompt=f'Generate News Article within the Keywords\nKeywords: {keywords}\nNews Article:',
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                n=self.n,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty
            )

            generated_content = model.choices[0].text.strip()
            finish_reason = model.choices[0].finish_reason

            return prettify(generated_content, finish_reason)
        except Exception as e:
            message = f'Something went wrong with generating news article content, message: {e}'
            logging.error(message, exc_info=True)
