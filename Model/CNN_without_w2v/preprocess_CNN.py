import konlpy
import gensim
from konlpy.tag import Kkma, Mecab
from string import punctuation
import nltk
############################################## Notice ##############################################
# Konlpy 중 Kkma와 Twitter만 제대로 형태소 분석을 할 수 있음
# 여기서는 Twitter 데이터가 아닌 정형화된 질의어를 사용하므로, 꼬꼬마 형태소 분석기 활용
# TODO Mecab이 정확도가 더 좋고, 사용자 사전이 추가 가능하다고 하여 해당 분석기 사용해보기

class preprocessor :
    def __init__(self, tokenizer=Kkma()):
      self.tokenizer = tokenizer
      self.keyTagger = ['NNG', 'NNP', 'NNB', 'NNM', 'NR', 'NP', 'VV', 'VA'] # 추후 Tagger 중 중요한 품사 추가하거나, 덜 중요한 품사 제외
      # self.grammer = """
      #         NP : {<N.*>*<Suffix>?}
      #         VP : {<V.*>*}
      # """
    ## 전처리 만들어야 하는것
    # 1) stemmer
    # 2) stopwards
    # 3) tokenizer / 형태소 분석
    # 4) TFIDF
    def tokenize (self, sentence):
        return self.tokenizer.morphs(self.strip_punctuation(sentence))

    def postTagging (self, sentence):
        return self.tokenizer.pos(self.strip_punctuation(sentence))

    def keywordExtractor (self, sentence): # 중요 단어만 추리기 (Noun, Verb 위주)
        words = [word for word, tag in self.postTagging(sentence) if tag in self.keyTagger]
        # parser = nltk.RegexpParser(self.grammer)
        return words

    def keywordListExtractor (self, dataset):
        keword_list = []
        criteria = int(len(dataset)/10)
        percent = 0
        for idx, item in enumerate(dataset) :
            if idx % criteria == 0 :
                print("%d%% of sentence's has been post-tagged" % percent)
                percent += 10
            keword_list.append(self.keywordExtractor(item[0])) # konlpy로 분석해서 형태소별로 중요한 단어만 남기기
        return keword_list

    def strip_punctuation(self, s): # 특수문자 제거
        return "".join(c for c in s if c not in punctuation)


# mecab = Mecab()
# mecab.tagger = Tagger()
# pre_pro = preprocessor()
#
# sentence = "보험계약대출도 인지세가 입니다"
# print(pre_pro.tokenize(sentence))
# print(pre_pro.postTagging(sentence))
# print(pre_pro.keywordExtractor(sentence))