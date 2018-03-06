# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from bs4 import BeautifulSoup
import json

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"}
#获取cookie
def Get_cookie():
    browser = webdriver.Chrome()
    try:
        browser.get("https://weibo.com/")
        WebDriverWait(browser,20).until(
            EC.element_to_be_clickable((By.XPATH,'//span[@node-type="submitStates"]'))
            )
    except:
        print("页面未加载完全")
    try:
        username = browser.find_element_by_xpath('//input[@id="loginname"]')
        password = browser.find_element_by_xpath('//input[@type="password"]')
        button = browser.find_element_by_xpath('//span[@node-type="submitStates"]')
    except:
        print("webelement定位错误")
    username.clear()
    username.send_keys("yourusername")
    password.clear()
    password.send_keys("yourpassword")

    #判断是否有验证码
    locate_verifycode = 0
    try:
        WebDriverWait(browser,5).until(
            EC.visibility_of_element_located((By.XPATH,'//img[@node-type="verifycode_image"]'))
            )
    except:
        print("无验证码")
        locate_verifycode = 1
    if locate_verifycode == 0:
        verifycode = browser.find_element_by_xpath('//input[@name="verifycode"]')
        print("请输入验证码")
        verifycode_text = input()
        verifycode.clear()
        verifycode.send_keys(verifycode_text)
    button.click()
    try:
        WebDriverWait(browser,10).until(
            EC.title_is("我的首页 微博-随时随地发现新鲜事")
            )
        #print(browser.current_url)
    except:
        print("跳转首页异常")
    cookie = [item["name"] + "=" + item["value"] for item in browser.get_cookies()]  
    #print(cookie)
    cookie_str = ';'.join(item for item in cookie)
    #print(cookie_str)
    browser.close()
    return cookie_str

cookies_dict = {'cookie':Get_cookie()}
cookies = requests.utils.cookiejar_from_dict(cookies_dict,cookiejar =None, overwrite = True)
session = requests.Session()
session.cookies = cookies
url = 'https://weibo.com/aj/v6/comment/big?id=4214105206718357&page={}&filter=hot&f'

#循环遍历API
def traversal():
    pagenum = 1
    start_url = url.format(str(pagenum))
    response = session.get(start_url,headers = headers)
    response.encoding = response.apparent_encoding
    #print(response.text)
    #print(response.status_code)
    totalpage_pattern = re.compile(r'"totalpage":([0-9]*?),')
    totalpage = re.findall(totalpage_pattern,response.text)[0]
    #print(totalpage)
    #print(pagenum)
    while pagenum <= int(totalpage):
        temp = session.get(url.format(pagenum))
        print(url.format(pagenum))
        temp.encoding = temp.apparent_encoding
        print("正在提取"+str(pagenum)+'页的内容')
        #print(temp.text)
        extract(temp.text)
        pagenum = pagenum +1

#提取函数
def extract(content):
    pattern = re.compile(r'\：(.*)')
    json_text = json.loads(content)
    text = json_text.get("data").get("html")
    text_bsobj = BeautifulSoup(text,'html.parser')
    tags = text_bsobj.find_all('div',{"class":"WB_text"})
    for tag in tags:
        WB_text = re.findall(pattern,tag.text)[0]
        Write(WB_text)

#写入函数
def Write(WB_text):
    try:
        f = open("F:\学习\临时\献给周总理.txt",'a')
        f.write(WB_text)
    finally:
        f.close()

traversal()
print("成功写入文件！")

#绘制词云
