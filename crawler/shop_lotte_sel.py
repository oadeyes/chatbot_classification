from selenium import webdriver
from bs4 import BeautifulSoup
import codecs
from lxml import html
import urllib.request
import urllib.parse


# driver = webdriver.Chrome('/home/alice/chromedriver')

# driver = webdriver.Chrome(executable_path=r"/home/alice/chromedriver/chromedriver")
# driver.implicitly_wait(3)
# driver.get('https://nid.naver.com/nidlogin.login')

MASTER_URL = "http://www.lotte.com"

all_data = []
domain = {'보험': 0 , '쇼핑': 1, '전자' : 2}
file_name = "lotteshopping_question.txt"

def getWebSource (web_url) :
    with urllib.request.urlopen(MASTER_URL+web_url) as response:
        response.encoding = 'utf8'
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
    return soup, response

soup, resp = getWebSource("/custcenter/searchFaqTypeList.lotte?sub_cd=1444&bbc_no=19067")
init_parsed = soup.select("div.faq_list > ul > li > dl > dd > a")

faq_category = []
for link in init_parsed :
    faq_category.append((link.string, link.get("href")))

for cat_name, cat_url in faq_category:
    soup_cat, resp_cat = getWebSource(faq_category[0][1])
    cat_parsed_question = soup_cat.select("table.board-list-gud > tbody > tr > td.delivery > a")
    cat_parsed_reply = soup_cat.select("table.board-list-gud > tbody > tr > td.viewreply")

    question = []
    reply = []
    for que in cat_parsed_question :
        question.append(que.text)

    for rep in cat_parsed_reply:
        item = []
        reply_item = rep.find_all("div", class_=lambda x: x != 'rating_box')
        reply_item_detail = rep.find_all("p", class_=lambda x: x != 'rating_box')[:-2]
        item.append(" ".join([item1.text for item1 in reply_item if len(item1) > 1]))
        item.append(" ".join([item2.text for item2 in reply_item_detail if len(item2) > 1]))
        reply.append(" ".join(item))


    for idx in range(len(question)):
        all_data.append((question[idx], reply[idx], domain['쇼핑']))
# print(len(all_data))
f = codecs.open('/home/alice/yeongmin/' + file_name, 'w', encoding='utf8')
for idx in range(len(all_data)):
    f.write(str(all_data[idx][0])+"\n")
f.close()

