from selenium import webdriver
from bs4 import BeautifulSoup
import codecs
from lxml import html
import urllib.request
import urllib.parse
import re

driver = webdriver.PhantomJS('/home/alice/yeongmin/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
# driver = webdriver.Chrome('/home/alice/chromedriver')

# driver = webdriver.Chrome(executable_path=r"/home/alice/chromedriver/chromedriver")
driver.implicitly_wait(3)
driver.get('https://nid.naver.com/nidlogin.login')

# MASTER_URL = "http://www.interpark.com"
#
# # http://www.interpark.com/ecenter/MainFAQ.do?_method=MainFAQSearch&faq1st=FAQS04&selType=1
#
# all_data = []
# domain = {'보험': 0 , '쇼핑': 1, '전자' : 2}
# file_name = "interpark.txt"
#
# def getWebSource (web_url) :
#     with urllib.request.urlopen(MASTER_URL+web_url) as response:
#         response.encoding = 'utf8'
#         html = response.read()
#         soup = BeautifulSoup(html, 'html.parser')
#     return soup, response
# #
# # soup, resp = getWebSource("/ecenter/MainFAQ.do?_method=MainFAQSearch")
# #
# # faq_list_all = []
# # faq_list = soup.find_all(id=re.compile("^faq_li"))
# # for idx, faq_type in enumerate(faq_list):
# #     detail_list = faq_type.select("li")
# #     for item in detail_list:
# #         faq_list_all.append(( item.get("id"), idx+1))
