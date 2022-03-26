
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
import time
import re


def urlProcess(word):
    
    file = open(f'./data/{word}_fiddler.txt','r',encoding='utf-8')
    if file==None:
        print(f'未找到./data/{word}_fiddler.txt')
        print('------------------------------------\n')
        print('请检查修改您的默认fiddler文件保存位置,file->save->selected all sessions->as text')
        print('如果selected all sessions为灰色无法选择 -> 请随意点击小红书小程序创造数据,在fiddler中全选(见视频描述)')
        print('将其默认保存路径手动改为该文件夹下/data,以便后续使用')
        print('\n------------------------------------\n')
        
        print(f'对于该文件: {word}_fiddler.txt')
        print(f'您可将它移动到/data文件夹下,执行如下命令以单独解析此文件')
        print(f'\n python main.py {word} -f \n')
        exit(0)
    file_data = file.read()
    
    base_url = "https://www.xiaohongshu.com/discovery/item/"
    
    pattern = re.compile(r'"se_pr":"([\d\w]*)"',re.U)
    ids = pattern.findall(file_data)
    
    url = []
    for id in ids:
        if len(id)==24:
            url.append(base_url+id)
    
    url = list(set(url))
    print(f'{word}文章的有效地址数量为: {len(url)}')
    return url
    

def startBrower():
    opt = Options()
    opt.add_argument('--no-sandbox')                # 解决DevToolsActivePort文件不存在的报错
    opt.add_argument('--disable-gpu')               # 谷歌文档提到需要加上这个属性来规避bug
    opt.add_argument('blink-settings=imagesEnabled=false')      # 不加载图片，提升运行速度
    #opt.add_argument('--headless')                  # 浏览器不提供可视化界面。Linux下如果系统不支持可视化不加这条会启动失败
    opt.add_experimental_option('excludeSwitches', ['enable-logging'])

    brower = webdriver.Chrome(options=opt)
    return brower

def getXHScontent(word):
    URL = urlProcess(word)
    articles = []
    brower = startBrower()
    
    for id,url in enumerate(URL):
        if id%20==0:
            print('---------------------')
            print(f'已完成 {id}/{len(URL)}')
            print('---------------------')
        print(f'正在访问{url}')
        brower.get(url)
        time.sleep(3)
        article = ""
        contents_1 = brower.find_elements(by=By.TAG_NAME,value="p")
        contents_2 = brower.find_elements(by=By.CLASS_NAME,value="as-p")
        for content in contents_1:
            words = content.text
            if words.find("一起来分享给朋友们看看吧")==-1:
                article+=words
            else:
                break
        for content in contents_2:
            words = content.text
            article+=words
        print(f'文章字数: {len(article)}')
        if len(article)==0:
            continue
        articles.append({
            "url":url,
            "content":article
        })
    print('---------------------')
    print(f'有效文章数量为{len(articles)}')
    print('---------------------')
    return articles

