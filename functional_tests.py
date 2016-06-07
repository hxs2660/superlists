#!/usr/bin/env python3
#codeing:utf-8
from selenium import webdriver
import time
browser=webdriver.PhantomJS(executable_path='./phantomjs')
browser.get('http://localhost:8000')
assert 'Django' in browser.title
#print(browser.page_source)
browser.close()
