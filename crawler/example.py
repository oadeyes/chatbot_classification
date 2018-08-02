from bs4 import BeautifulSoup
from lxml import html
import urllib.request
import urllib.parse

def getWebSource (web_url) :
    with urllib.request.urlopen(web_url) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

    return soup, response

soup, resp = getWebSource("http://www.lotte.com/custcenter/searchFaqTypeList.lotte?sub_cd=1444&bbc_no=19067")
init_parsed = soup.find("table", {"class": "board-list-gud"})
question = init_parsed.find_all("td", {"class": "delivery"})
reply = init_parsed.find_all("td", {"class": "viewreply"})
# print(question)
# print(reply)
# print(soup.find_all("div"))


lxml_html = html.fromstring(resp.text)
print(lxml_html.find_class("board-list-gud").text_content())
# request.post("https://www.samsunglife.com/erms/api/proxy/apiProxyAjax.do")