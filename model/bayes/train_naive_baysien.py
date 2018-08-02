from naive_bayesian import BayesianFilter
from data_loader import text_data
import random

data = text_data().train_data

for idx in range(5): ## TODO 일단 이건 빈도 기반 naive Bayes,, word2vec 사용해서 다시 할 예정
    random.shuffle(data)

    train_data = data[:4000]
    test_data = data[4000:]

    bf = BayesianFilter()

    for item in train_data:
        bf.fit(item[0], item[1])

    cnt = 0
    for item in test_data:
        pre, score_list = bf.predict(item[0])
        if item[1] in pre:
           cnt += 1
        # print("질문", item[0])
        # print("예측 결과 =", pre," | 기존 결과 = ",item[1])
        # print(score_list)
        # print("==========================================================================================================================")
    print("test data = ",len(test_data)," cnt = ", cnt," accuracy = %0.3f " % (cnt/len(test_data)))

# ==================================================    결과물    ==========================================================
# test data =  1694  cnt =  1539  accuracy = 0.909
# test data =  1694  cnt =  1537  accuracy = 0.907
# test data =  1694  cnt =  1530  accuracy = 0.903
# test data =  1694  cnt =  1530  accuracy = 0.903
# test data =  1694  cnt =  1549  accuracy = 0.914
# ==========================================================================================================================
