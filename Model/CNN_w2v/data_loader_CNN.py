import os, nltk, time, codecs
import random, math
import numpy as np
from ast import literal_eval
from collections import Counter
import pandas as pd
from preprocess_CNN import preprocessor


class text_data(object):
    def __init__(self, path="/home/alice/yeongmin/raw_data", max_vocab=40000, max_len=100, end_token="<eos>"):
        self.train_pt, self.val_pt, self.test_pt = 0, 0, 0
        self.path = path
        self.max_len = max_len
        self.max_vocab = max_vocab
        self.w2v_model_len = 200

        self.w2idx = {end_token: 0, "<unk>": 1}
        self.res2idx = {}

        self.train_ids, self.train_len, self.train_label = self.files_to_ids(path+'/train/bot_dataset.txt', 'train')
        self.test_ids, self.test_len, self.test_label = self.files_to_ids(path+'/test/bot_dataset.txt', 'test')

        self.vocab_size = len(self.w2idx)

        self.train_size = len(self.train_ids)
        self.test_size = len(self.test_ids)

        self.idx2w = {}
        for word in self.w2idx:
            self.idx2w[self.w2idx[word]] = word

        self.idx2res = {}
        for cat in self.res2idx:
            self.idx2res[self.res2idx[cat]] = cat

    def files_to_tupes(self, path):
        f = codecs.open(path, 'r', encoding='utf8')
        data_set = []
        while True:
            line = f.readline().strip()
            if not line: break
            item = literal_eval(line.replace("&quot",""))
            data_set.append(item)
        f.close()
        return data_set

    def get_w2idx(self, word):
        return 1 if word not in self.w2idx else self.w2idx[word]

    def files_to_ids(self, path, opt):
        print (" - Read files from: {}".format(path))

        length, ids, label = [], [], []

        dataset = self.files_to_tupes(path)
        random.shuffle(dataset)
        pre_pro = preprocessor()
        post_tagged = pre_pro.keywordListExtractor(dataset)  # konlpy로 분석해서 형태소별로 중요한 단어만 남기기  # TODO Stemming / Stopword 등 처리하기
        raw_label = [item[1] for item in dataset]
        print(raw_label)

        if "train" in opt:
            for idx, category in enumerate(list(set([item[1] for item in dataset]))):
                self.res2idx[category] = idx
        print(self.res2idx)
        for num, tagged in enumerate(post_tagged):
            id = np.zeros(shape=[self.max_len, self.w2v_model_len], dtype=np.float32) # TODO 우선은 max 길이로 하고, 나중에는 중간에 translate 할 수 있는 layer 달아주던지, 다른 방법 고민해보기,,
            # line += " <eos>" # TODO 나중에 RNN / LSTM 적용할 때 다시 켜기, 지금은 Sequence 상관 없음
            words = pre_pro.wordListToVectorList(tagged) # word list를 벡터 list로 변경
            for i, word_vec in enumerate(words):
                if i == self.max_len:  # N개보다 클 경우 잘라주기
                    break
                id[i] = word_vec # np.array에 해당 값 추가
            ids.append(id)
            length.append(min(len(words), self.max_len))
            label.append(self.res2idx[raw_label[num]]) # TODO  모델부-loss function에 One-hot Encoding 되어 있는 것으로 보임 / 우선은 카테고리를 숫자 형태로 1개만 넣어보자! && Loss function 분석하기

        return np.array(ids), np.array(length), np.array(label)

    def get_train(self, batch_size=20):
        pt = self.train_pt
        self.train_pt = (self.train_pt + batch_size) % self.train_size
        return self.train_ids[pt: pt+batch_size], self.train_len[pt: pt+batch_size], self.train_label[pt: pt+batch_size]

    def get_test(self, batch_size=20):
        pt = self.test_pt
        self.test_pt = (self.test_pt + batch_size) % self.test_size
        return self.test_ids[pt: pt+batch_size], self.test_len[pt: pt+batch_size], self.test_label[pt: pt+batch_size]



# 일단 뭐로 분석할까가 문제네,
# Naive Bayesian
# 1) 일단은 가져와서, 형태소 분석하는거 먼저
# 2-1) 그리고 Stemming 작업
# 3) Counter Vectorizer로 단어별 카운트 세기
# 4) Naive Bayesian 알고리즘 돌리기
# 5) 결과값 출력하기
#
# data = text_data()
# print(len(data.train_ids))
# print(data.train_ids[0])