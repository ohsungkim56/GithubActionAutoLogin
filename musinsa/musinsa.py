import sys
from os import getenv
from urllib.parse import quote
import requests as req
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def setup():
    global url
    url = "https://my.musinsa.com/login/v1/login"

    global data
    data = {"referer" : "", "isCheckGoogleRecaptcha" : "false", "id" : getenv("MUSINSA_ID"), "pw" : getenv("MUSINSA_PW")}
    
    kwargs = {}
       
    kwargs['headers'] = {'Host':'my.musinsa.com',
    'Connection':'keep-alive',
    'Cache-Control':'max-age=0',
    'Upgrade-Insecure-Requests':'1',
    'Origin':'https://my.musinsa.com',
    'Content-Type':'application/x-www-form-urlencoded',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'}

    kwargs['cert'] = ("CA.csr", "priv.pem")
    
    kwargs['verify']=False
    
    #kwargs['proxies'] = {"http":"http://127.0.0.1:8888", "https":"https://127.0.0.1:8888"}
    
    return kwargs

def login(url, data, kwargs={}):
    try:
        res = req.post(url, data=data, **kwargs)
        return res
    except Exception as e:
        print(e)
        sys.exit(1)
        
def check(res):
    if res.status_code != 200:
        print("login fail - response code(%d)"%res.status_code)
        sys.exit(1)
    elif "alert" in res.text:
        print("login fail - not expected response")
        print(res.text)
        sys.exit(1)
    else:
        print(res.text)

def main():
    kwargs = setup()
    res = login(url, data, kwargs=kwargs)
    check(res)
    sys.exit(0)
    
if __name__ == "__main__":
    main()
    