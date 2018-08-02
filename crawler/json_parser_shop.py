import json
import requests
import codecs


def getData (url):
    response = requests.get(url)
    response.encoding = 'utf8'
    result = response.json()
    return json.loads(result['contents'])['data']

all_data = []
domain = {'보험': 0 , '쇼핑': 1, '전자' : 2}
file_name = "samsunglife.txt"

for i in range(200) :
    data_que = getData("http://www.samsunglife.com/erms/api/proxy/apiProxyAjax.do?service=faq&command=getFaqList&form=kb&pageNo=" + str(i) + "&childrenNodeId=NODE0000000003")
    for item_que in data_que :
        title = item_que['title']
        kb_id_que = item_que['kb_id']
        node_id_que = item_que['node_id']
        data_ans = getData("http://www.samsunglife.com/erms/api/proxy/apiProxyAjax.do?service=faq&command=getFaqContentsById&form=kb&kbId=" + kb_id_que + "&nodeId=" + node_id_que + "&serviceType=SVFAQ")
        answer = []
        for ans_item in data_ans :
            answer.append(ans_item['contents'])
        all_data.append((title, answer, domain['보험']))

# 파일 저장하는 부분
f = codecs.open('/home/alice/yeongmin/'+file_name, 'w', encoding='utf8')
f.write(str(all_data)+"/n")
f.close()

