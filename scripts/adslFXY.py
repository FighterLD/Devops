# coding:utf-8
'''
Created on 2016年8月12日

@author: liudong
主要用于宽带拨号
路由器管理后台地址：http://192.168.3.1/
用户名：admin
密码：123456.com

拨号宽带账号信息
宽带账号：CD@02883330727@SP
宽带密码：83330727
'''
from splinter import Browser
from time import sleep

browser = Browser('chrome')
browser.visit('http://192.168.3.1')

browser.find_by_css('input[type=text]')[0].fill('admin')
browser.find_by_css('input[type=password]')[0].fill('Pinbot123')

login_btn = browser.find_by_css('input[type=submit]')[0]
login_btn.click()

interface_btn = browser.find_by_xpath('//*[@id="menuMainList"]/li[1]/div/ul/li[2]/span/a')[0]
interface_btn.click()

disconnect_btn = browser.find_by_css('input[type=submit]')[0]
disconnect_btn.click()
alert = browser.get_alert()
print alert.text
alert.accept()

print "确定"
connect_btn = browser.find_by_css('input[type=submit]')[0]
connect_btn.click()

#browser = Browser('chrome')
#browser.visit('http://192.168.0.1')
#
#browser.find_by_css('input[type=text]')[0].fill('admin')
#browser.find_by_css('input[type=password]')[0].fill('123456.com')
#login_btn = browser.find_by_xpath('//*[@id="login"]/tbody/tr[2]/td[3]/ul/li/a')[0]
#login_btn.click()
#interface_btn = browser.find_by_xpath('//*[@id="id_Interfaces"]')[0]
#interface_btn.click()
#btn = browser.find_by_xpath('//*[@id="content"]/table[3]/tbody[9]/tr/td[1]/a[2]')[0]
#print btn.html
#btn.click()
#btn.click()
#sleep(5)
#browser.quit()
