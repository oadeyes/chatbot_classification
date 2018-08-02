import codecs, json
from ast import literal_eval

## 대열 프로님 json parsing
def kyobo_parser():
    raw_data = ["data_sum.txt",]
    
    f = codecs.open('/home/alice/yeongmin/raw_data/kyobo_raw_cleaned.json', 'r', encoding='utf8')
    lines = []
    # with open('/home/alice/yeongmin/raw_data/kyobo_raw_cleaned.json', "r", encoding='utf8') as fin:
    while True:
        line = f.readline()
        if not line: break
        lines.append(line)
    f.close()
    
    result = json.loads(" ".join(lines))
    
    file_name = "kyobo_question.txt"
    f = codecs.open('/home/alice/yeongmin/' + file_name, 'w', encoding='utf8')
    for idx in range(len(result)):
        f.write(str(result[idx]['ttl'])+"\n")
    f.close()

## 각 파일에서 데이터 호출해서 Tuple로 만드는 함수
def data_merge():
    raw_data = dict()
    # 각 카테고리별 호출, 파일 및 카테고리 추가시 추가 삽입
    domain = ['life', 'svc', 'shp', 'tour']
    life_raw_data = ['samsunglife_question.txt','kyobo_question.txt']
    svc_raw_data = ['lg_svc_faq.txt','sec_svc_faq.txt']
    shp_raw_data = ['lotteshopping_question.txt', 'interpark_question.txt']
    tour_raw_data = ['modetour_questions.txt', 'hana_tour_faq.txt']
    raw_data[domain[0]] = life_raw_data
    raw_data[domain[1]] = svc_raw_data
    raw_data[domain[2]] = shp_raw_data
    raw_data[domain[3]] = tour_raw_data
    
    ## Read files
    result = []
    for domain_name in domain:
        for file_name  in raw_data[domain_name]:
            f = codecs.open('/home/alice/yeongmin/raw_data/'+file_name, 'r', encoding='utf8')
            print(file_name," read begins")
            idx = 0
            miss_cnt = 0
            while True:
                line = f.readline().strip()
                if not line:
                    miss_cnt += 1
                    if miss_cnt > 3: break
                    continue
                else :
                    miss_cnt = 0
                result.append((line.replace("\n"," "), domain_name))
                idx += 1
            print("total %d lines has been recorded" % idx)
            f.close()

    file_name = "bot_dataset_0802.txt"
    f = codecs.open('/home/alice/yeongmin/' + file_name, 'w', encoding='utf8')
    for idx in range(len(result)):
        f.write(str(result[idx][0])+"\n")
    f.close()

data_merge()