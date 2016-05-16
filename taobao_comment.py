import json
import re
from bs4 import BeautifulSoup
import requests

__author__ = 'liebesu'

def get_category(url):
    r=requests.get(url)
    soup=BeautifulSoup(r.content,"html.parser")
    category=soup.find('script',text=re.compile('g_page_config'))
    json_text = re.search(r'^\s*g_page_config\s*=\s*({.*?})\s*;\s*$',
                      category.string, flags=re.DOTALL | re.MULTILINE).group(1)
    print json_text
    category_json=json.loads(json_text)
    print category_json
    for item in category_json['mods']['itemlist']['data']['auctions']:
        print item['raw_title']
        print item['detail_url']
        print item['user_id']
        print item['nick']

        get_comment_image(item['nid'],item['user_id'])
        exit()
def get_comment_image(item_id,user_id):
    header={'Referer':'https://www.taobao.com',
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'}
    cookie={'v':'0', 'thw':'cn','cna':'Osm6D3jDRXYCATFB9MyzoDKI','cookie2':'1cf03d604570666062a27eaf51b4f346', 't':'3aec712fba5fb4607ef2d0035c791ff4', 'uc1':'cookie14=UoWxMkAwwQtw8Q%3D%4D', 'l':'An5-hE0K5/9cC4uVpW/NAh0DTp7Av0I5'}

    proxy={'http':"1.63.18.22:8080"}
    url='https://rate.taobao.com/feedRateList.htm?auctionNumId='+item_id+'&userNumId='+user_id+'&currentPageNum=1&pageSize=20&rateType=&orderType=sort_weight&showContent=1&attribute=&sku=&hasSku=false&folded=0&callback=jsonp_tbcrate_reviews_list'
    r=requests.get(url,proxies=proxy,headers=header,cookies=cookie)
    print r.content


def get_item(url):
    r=requests.get(url)
    a=open('test/test.html','w')
    a.write(r.content)
    a.close()
if __name__=='__main__':
    url='https://s.taobao.com/search?q=%E6%A0%91%E8%8E%93%E6%B4%BE'
    get_category(url)
