import requests
r=requests.Session()
url="https://www.taobao.com/"
re=r.get(url)
print re.cookies