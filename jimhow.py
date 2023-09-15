# 用到的库
import os
import requests
import re
from bs4 import BeautifulSoup
import time
import urllib.request
from pywebio.input import *
from pywebio.output import *

#洛谷题目和答案的网址
P = []
urlp = "https://www.luogu.com.cn/problem/"
urls = "https://www.luogu.com.cn/problem/solution/"
savedate = "./"
fn = ""

#前端的接口
def jim():
    name = select('请输入你的题目难度', ['入门', '普及-', '普及/提高-', '提高+/省选-', '省选/NOI-', 'NOI/NOI+/CTSC'])
    if name == "入门":
        ii=1
    elif name == "普及-":
        ii=2
    elif name == "普及/提高-":
        ii=3
    elif name == "提高+/省选-":
        ii = 4
    elif name == "省选/NOI-":
        ii = 5
    elif name == "NOI/NOI+/CTSC":
        ii = 6
    return ii
    #根据用户选择进入目标网页

# 获取符合需求的题目序号
def getlist(url):
    #伪装者，反爬
    headers = {
        "Cookie": "client_id=98cfc2cc86d451827cf762d426dc1b5e5551a763; login_referer=https%3A%2F%2Fwww.luogu.com.cn%2Fproblem%2FP1000; _uid=561385",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    response = requests.get(url=url, headers=headers)
    # print(response.text)
    html = response.text
    pattern = re.compile(r'(<a\shref=".*?">)*?')
    problemlist = re.findall(pattern, response.text)
    for x in problemlist:
        if (x != ""):
            P.append(x[9:14])

# 获得题目
def getproblem(url):
    # 发送请求部分
    headers = {
        "Cookie": "client_id=98cfc2cc86d451827cf762d426dc1b5e5551a763; login_referer=https%3A%2F%2Fwww.luogu.com.cn%2Fproblem%2FP1000; _uid=561385",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    response = requests.get(url=url, headers=headers)
    html = response.text
    # 把数据整理干净
    bs = BeautifulSoup(html, "html.parser")
    core = bs.select("article")[0]
    md = str(core)
    md = re.sub("<h1>", "# ", md)
    md = re.sub("<h2>", "## ", md)
    md = re.sub("<h3>", "#### ", md)
    md = re.sub("</?[a-zA-Z]+[^<>]*>", "", md)
    # 保存数据
    global fn
    fn = bs.title.string
    fn = fn[:-5]
    savedate = "./"
    savedate = savedate + fn
    if not os.path.exists(savedate):
        os.mkdir(savedate)
    filename = savedate + '/' + fn + ".md"
    with open(filename, "w", encoding="utf-8") as fp:
        fp.write(md)

# 获取题目的解答
def getsolution(url):
    # 发送请求
    headers = {
        "Cookie": "__client_id=7298f81227f1bc2d6e646cba05a73571d5f5ac0c; _uid=1091435",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    response = requests.get(url=url, headers=headers)
    # 整理数据
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    encoded_content_element = soup.find('script')
    encoded_content = encoded_content_element.text
    start = encoded_content.find('"')
    end = encoded_content.find('"', start + 1)
    encoded_content = encoded_content[start + 1:end]
    decoded_content = urllib.parse.unquote(encoded_content)
    decoded_content = decoded_content.encode('utf-8').decode('unicode_escape')
    start = decoded_content.find('"content":"')
    end = decoded_content.find('","type":"题解"')
    decoded_content = decoded_content[start + 11:end]
    # 保存数据
    savedate = "./"
    savedate = savedate + fn
    if not os.path.exists(savedate):
        os.mkdir(savedate)
    filename = savedate + '/' + fn + "-题解" ".md"
    with open(filename, "w", encoding="utf-8") as fp:
        fp.write(decoded_content)

def main():
    # 获取需要的题号
    ii=jim()
    ans=input("你想下载几道题目")
    urll="https://www.luogu.com.cn/problem/list?tag=&difficulty="+str(ii)+"&page=1"
    put_text("开始下载,并且直接下载到代码所在文件，过程很慢，请耐心等待")
    getlist(urll)
    count = 0#记录爬取的题目数量
    for i in range(len(P)):
        print(P[i])
        count += 1
        getproblem(urlp + P[i])
        time.sleep(5)
        getsolution(urls + P[i])
        time.sleep(5)
        put_text("成功爬取第"+str(count)+"题")
        if (count >= int(ans)):#再爬就不礼貌了
            put_text("爬取完毕")
            break

if __name__ == "__main__":
    main()