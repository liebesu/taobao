#encoding=utf8
import argparse
import json
import os
import re
import urllib
from bs4 import BeautifulSoup
import requests
import sys
__author__ = 'liebesu'

reload(sys)
sys.setdefaultencoding('utf8')   
def get_category(name,url):
    r=requests.get(url)
    soup=BeautifulSoup(r.content,"html.parser")
    category=soup.find('script',text=re.compile('g_page_config'))
    json_text = re.search(r'^\s*g_page_config\s*=\s*({.*?})\s*;\s*$',
                      category.string, flags=re.DOTALL | re.MULTILINE).group(1)
    category_json=json.loads(json_text)
    for item in category_json['mods']['itemlist']['data']['auctions']:
        print item['raw_title']
        print item['detail_url']
        print item['user_id']
        print item['nick']

        get_comment_json(name,item['nid'],item['user_id'])

def get_comment_json(name,item_id,user_id):
    header={'Referer':'https://www.taobao.com',
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'}
    cookie={'v':'0', 'thw':'cn','cna':'Osm6D3jDRXYCATFB9MyzoDKI','cookie2':'1cf03d604570666062a27eaf51b4f346', 't':'3aec712fba5fb4607ef2d0035c791ff4', 'uc1':'cookie14=UoWxMkAwwQtw8Q%3D%4D', 'l':'An5-hE0K5/9cC4uVpW/NAh0DTp7Av0I5'}

    proxy={'http':"27.115.75.114:8080"}
    for n in range(1,10):
        url='https://rate.taobao.com/feedRateList.htm?auctionNumId='+item_id+'&userNumId='+user_id+'&currentPageNum='+str(n)+'&pageSize=20&rateType=&orderType=sort_weight&showContent=1&attribute=&sku=&hasSku=false&folded=0&callback=jsonp_tbcrate_reviews_list'
        r=requests.get(url,proxies=proxy,headers=header,cookies=cookie)
        if "jsonp_tbcrate_reviews_list" in r.content:
            reviews=r.content.replace("jsonp_tbcrate_reviews_list(","").replace(")","").decode("gbk").encode("utf-8")
            print reviews
            json_reviews=json.loads(reviews,encoding="utf-8")
            file_save(name,item_id,user_id,json_reviews)
        else:
            pass
def file_save(name,item_id,user_id,json):
    #name=name.dencode("").encode("utf-8")
    if os.path.exists(os.path.join(name,item_id+"_"+user_id)):
        pass
    else:
        os.makedirs(os.path.join(name,item_id+"_"+user_id))
    for auction in  json['comments']:
        if auction['photos']:
            for photo in  auction['photos']:
                urllib.urlretrieve("http:"+photo['url'].relpace("400x400","800x800"),os.path.join(name,item_id+"_"+user_id,os.path.basename(photo['url'])))







def get_item(url):
    r=requests.get(url)
    a=open('test/test.html','w')
    a.write(r.content)
    a.close()
if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument("s",help="input commodity name")
    arg=parser.parse_args()
    name=arg.s
    #url='https://s.taobao.com/search?q=树莓派3'
    url='https://s.taobao.com/search?q='+name
    get_category(name,url)
