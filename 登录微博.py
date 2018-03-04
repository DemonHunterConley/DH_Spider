# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests


browser = webdriver.Chrome()
try:
    browser.get("https://weibo.com/")
    WebDriverWait(browser,10).until(
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
username.send_keys("youruesrname")
password.clear()
password.send_keys("yourpassword")

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
print(cookie_str)

cookies = {'cookie':cookie_str}
session = requests.Session()
response = session.get("https://weibo.com/u/XXXXX/home",cookies = cookies)
response.encoding = response.apparent_encoding
print(response.text)
