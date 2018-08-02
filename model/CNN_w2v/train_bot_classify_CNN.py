import os

import tensorflow as tf
import numpy as np
import time

from bot_classify_CNN_model import Model
from data_loader_CNN import text_data
from preprocess_CNN import preprocessor

data = text_data()

def initialize_session():
    config = tf.ConfigProto()
    #config.gpu_options.allow_growth = True
    config.gpu_options.per_process_gpu_memory_fraction = 0.1
    return tf.Session(config=config)

##################################################
BATCH_SIZE = 20         # 배치 사이즈
num_k = 20              # 앞에 볼 단어 개수
num_cat = 4             # 카테고리 개수
emb_dim = 200            # 단어 embedding dimension
learning_rate = 0.0005  # Learning rate
use_clip = True         # Gradient clipping 쓸지 여부
##################################################

model = Model(num_k=num_k, emb_dim=emb_dim, vocab_size=data.vocab_size,
              use_clip=True, learning_rate=learning_rate)

sess = initialize_session()
sess.run(tf.global_variables_initializer())

def sample_test(test_input=""):
    pre_pro = preprocessor()
    post_tagged = pre_pro.keywordExtractor(test_input)
    words = pre_pro.wordListToVectorList(post_tagged)
    test_x = np.zeros(shape=(1, num_k, emb_dim), dtype=np.float32)
    for idx, word_vec in enumerate(words):
        if idx == num_k:  # N개보다 클 경우 잘라주기
            break
        test_x[0][idx] = word_vec
    out_x = sess.run(model.out_y, feed_dict={model.x: test_x})
    print(out_x[0], data.idx2res[out_x[0]])

def test_model():
    num_it = int(len(data.test_ids) / BATCH_SIZE)
    test_x = np.zeros((BATCH_SIZE, num_k, emb_dim), dtype=np.float32)
    mask = np.zeros(BATCH_SIZE, dtype=np.int32)
    test_loss, test_cnt = 0, 0

    for _ in range(num_it):
        test_ids, length, test_label = data.get_test(BATCH_SIZE)
        max_len = max(length)

        test_x.fill(0)
        mask.fill(0)

        for i in range(num_k - 1, max_len - 2):
            for batch in range(len(test_ids)):
                for j in range(0, num_k):
                    if i < j or i - j >= length[batch]:
                        break
                    test_x[batch][num_k - j - 1] = test_ids[batch][i - j]
                mask[batch] = 1 if length[batch] > i+1 else 0
                if length[batch] > i + 1:
                    input_y[batch] = test_label[batch]

            loss = sess.run(model.loss, feed_dict={model.x: test_x, model.y: input_y, model.mask: mask})
            test_loss += loss
            test_cnt += 1
    print("test loss: {:.3f}".format(test_loss / test_cnt))


input_x = np.zeros((BATCH_SIZE, num_k, emb_dim), dtype=np.float32)
input_y = np.zeros((BATCH_SIZE), dtype=np.int32)
input_mask = np.zeros(BATCH_SIZE, dtype=np.int32)
length = np.zeros(BATCH_SIZE, dtype=np.int32)

avg_loss, it_cnt = 0, 0
it_log, it_test, it_save, it_sample = 50, 250, 1000, 20
start_time = time.time()
iter_max = int(len(data.train_ids) / BATCH_SIZE)
for it in range(0, iter_max):
    train_ids, length, train_label = data.get_train(BATCH_SIZE)
    max_len = max(length)
    input_x.fill(0)
    for i in range(num_k - 1, max_len - 2):
        for batch in range(len(train_ids)):
            for j in range(0, num_k):
                if i < j or i-j >= length[batch]:
                    break
                input_x[batch][num_k-j-1] = train_ids[batch][i-j]
            input_mask[batch] = 1 if length[batch] > i+1 else 0

            if length[batch] > i + 1:
                input_y[batch] = train_label[batch]

        loss, _ = sess.run([model.loss, model.update],
                           feed_dict={model.x: input_x, model.y: input_y, model.mask: input_mask})
        avg_loss += loss
        it_cnt += 1

    # if it % it_log == 0:
    print(" it: {:4d} | loss: {:.3f} - {:.2f}s".format(it, avg_loss / 1, time.time() - start_time))
    avg_loss, it_cnt = 0, 0

    if it % it_test == 0 and it > 0:
        test_model()
    if it % it_save == 0 and it > 0:
        model.save(sess)
    if it % it_sample == 0 and it > 0:
        sample_test(test_input="보험계약대출도 인지세가 있나요")