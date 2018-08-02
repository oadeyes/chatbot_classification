import math, sys


class BayesianFilter:
    def __init__(self):
        self.words = set()  # 출현한 단어 기록
        self.word_dict = {}  # 카테고리마다의 출현 횟수 기록
        self.category_dict = {}  # 카테고리 출현 횟수 기록

    # 단어 tokenization --- (※1)
    def split(self, text):
        return text.split()

    # 단어와 카테고리의 출현 횟수 세기 --- (※2)
    def inc_word(self, word, category):
        # 단어를 카테고리에 추가하기
        if not category in self.word_dict:
            self.word_dict[category] = {}
        if not word in self.word_dict[category]:
            self.word_dict[category][word] = 0
        self.word_dict[category][word] += 1
        self.words.add(word)

    def inc_category(self, category):
        # 카테고리 계산하기
        if not category in self.category_dict:
            self.category_dict[category] = 0
        self.category_dict[category] += 1

    # 단어 추가 --- (※3)
    def fit(self, text, category):
        word_list = self.split(text)
        for word in word_list:
            self.inc_word(word, category)
        self.inc_category(category)

    # 단어 리스트에 점수 매기기--- (※4)
    def score(self, words, category):
        score = math.log(self.category_prob(category))
        for word in words:
            score += math.log(self.word_prob(word, category))
        return score

    # 예측 --- (※5)
    def predict(self, text):
        # 카테고리별 호출
        best_category = ""
        max_value = - 999999999999
        score_list = []
        for category in list(self.word_dict):
            cat_score = self.score(text.split(), category)
            score_list.append((category, cat_score))
            if max_value < cat_score:
                max_value = cat_score
                best_category = category

        return best_category, score_list

    # 카테고리 내부의 단어 출현 비율 계산 --- (※6)
    def word_prob(self, word, category):
        n = self.get_word_count(word, category) + 1  # ---(※6a)
        d = sum(self.word_dict[category].values()) + len(self.words)
        return n / d

    # 카테고리 내부의 단어 출현 횟수 구하기
    def get_word_count(self, word, category):
        if word in self.word_dict[category]:
            return self.word_dict[category][word]
        else:
            return 0

    # 카테고리 계산
    def category_prob(self, category):
        sum_categories = sum(self.category_dict.values())
        category_v = self.category_dict[category]
        return category_v / sum_categories