from selenium import webdriver
from bs4 import BeautifulSoup
import codecs
from lxml import html
import urllib.request
import urllib.parse
import re


# driver = webdriver.Chrome('/home/alice/chromedriver')

# driver = webdriver.Chrome(executable_path=r"/home/alice/chromedriver/chromedriver")
# driver.implicitly_wait(3)
# driver.get('https://nid.naver.com/nidlogin.login')

MASTER_URL = "http://www.interpark.com"

# http://www.interpark.com/ecenter/MainFAQ.do?_method=MainFAQSearch&faq1st=FAQS04&selType=1

all_data = []
domain = {'보험': 0 , '쇼핑': 1, '전자' : 2}
file_name = "interpark.txt"

def getWebSource (web_url) :
    with urllib.request.urlopen(MASTER_URL+web_url) as response:
        response.encoding = 'utf8'
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
    return soup, response

soup, resp = getWebSource("/ecenter/MainFAQ.do?_method=MainFAQSearch")

faq_list_all = []
faq_list = soup.find_all(id=re.compile("^faq_li"))
for idx, faq_type in enumerate(faq_list):
    detail_list = faq_type.select("li")
    for item in detail_list:
        faq_list_all.append(( item.get("id"), idx+1))

question = []
reply = []

for idx, (faq1st, selType) in enumerate(faq_list_all) :
    sc_page = 1
    max_page = 9999999

    while sc_page <= max_page:
        soup, _ = getWebSource("/ecenter/MainFAQ.do?_method=MainFAQSearch&faq1st="+faq1st+"&selType="+str(selType)+"&sc.page="+str(sc_page))
        faq_table = soup.select("table.tb_faqList")
        max_page = int(soup.select("div.div_faqList_bot02 > table > tr > td ")[0].text.strip()[-2])
        faq_ques = faq_table[0].find_all("tbody", id="tbody_ques")
        faq_rep = faq_table[0].find_all("table", attrs={"class":"box_freq_mid"})
        for item in faq_ques:
            question.append(item.find_all("td", attrs={"name":"title"})[0].text)

        for item in faq_rep:
            reply.append(item.select("tr > td")[0].text.strip())

        sc_page += 1

for idx in range(len(question)):
        all_data.append((question[idx].replace("\xa0", " "), reply[idx].replace("\xa0", " "), domain['쇼핑']))

f = codecs.open('/home/alice/yeongmin/'+file_name, 'w', encoding='utf8')
f.write(str(question[idx])+"\n")
f.close()
