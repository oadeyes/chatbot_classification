import os, nltk, time, codecs
import random
import numpy as np
from ast import literal_eval
from collections import Counter
# import konlpy
# from konlpy.tag import Hannanumkonlpy

class text_data(object):
    def __init__(self, path="/home/alice/yeongmin/raw_data", max_vocab=40000, max_len=100, end_token="<eos>"):
        self.train_pt, self.val_pt, self.test_pt = 0, 0, 0
        self.path = path
        self.max_len = max_len
        self.max_vocab = max_vocab

        self.w2idx = {end_token: 0, "<unk>": 1}
        # self.train_ids, self.train_len, self.train_label = self.files_to_ids(path+'/bot_dataset.txt', 'train')
        # self.test_ids, self.test_len, self.test_label = self.files_to_ids(path+'/bot_dataset.txt','test')

        self.train_data= self.files_to_tupes(path+'/bot_dataset.txt')

        self.vocab_size = len(self.w2idx)

        # self.train_size = len(self.train_ids)
        # self.test_size = len(self.test_ids)
        #
        # self.idx2w = {}
        # for word in self.w2idx:
        #     self.idx2w[self.w2idx[word]] = word


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

        lines = [item[0] for item in dataset] # TODO Stemming / Stopword 등 처리하기 / konlpy로 분석해서 형태소별로 중요한 단어만 남기기
        label = [item[1] for item in dataset] # TODO output도 아마 one-hot encoding으로 변경 해야 할 것

        if "train" in opt:
            word_count = Counter([word for line in lines for word in line.strip().split()])
            self.w2idx = word_count.most_common(self.max_vocab)

        for num, line in enumerate(lines):
            id = np.zeros(self.max_len, dtype=np.int32) # TODO 우선은 max 길이로 하고, 나중에는 중간에 translate 할 수 있는 layer 달아주던지, 다른 방법 고민해보기,,
            # line += " <eos>" # TODO 나중에 RNN / LSTM 적용할 때 다시 켜기, 지금은 Sequence 상관 없음
            words = line.split()
            for i, word in enumerate(words):
                if i == self.max_len:
                    break
                if word not in self.w2idx and len(self.w2idx) < self.max_vocab:
                    self.w2idx[word] = len(self.w2idx)
                id[i] = self.get_w2idx(word)
            ids.append(id)
            length.append(i)
            label.append(num % 2)

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