"""
author： flowerlake
time： 2019-08-19
description： 从MongoDB中抽取持久化的某个问题的所有回答，主要内容包括回答的内容的一些文本分析，还有人物关系等
"""
from collections import Counter
from Analysis_Module.GetFromDB import GetFromDB
import jieba, logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TextExtractor():

    def __init__(self, answers):
        self.answers = answers

    def split_word(self):
        with open("data/stopwords.txt", "r", encoding="utf-8") as f:
            stopwords = f.readlines()
        stopwords = [i.strip() for i in stopwords]

        logger.info("stopwords list: {}".format(stopwords[:5]))

        answer_sentence = "".join(" ".join(self.answers).split("，|。|？|！"))

        jieba_word = jieba.cut(answer_sentence)
        jieba_word = [i for i in jieba_word if i not in stopwords or i == " "]

        word_count = dict(Counter(jieba_word))

        word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        logger.info(word_count)

        return jieba_word




if __name__ == "__main__":
    test = GetFromDB()
    answers = test.get_content()
    textExtractor = TextExtractor(answers)
    textExtractor.split_word()
