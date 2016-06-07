#!/usr/bin/env python3
#codeing:utf-8

import unittest
from selenium import webdriver

class NewVisitorTest(unittest.TestCase):
    """docstring for NewVisittorTest"""
    #测试之前运行
    def setUp(self):
        self.browser=webdriver.PhantomJS(executable_path='../phantomjs')
        self.browser.implicitly_wait(3)

    #测试之后运行    
    def tearDown(self):
        self.browser.quit()

    #测试方法    
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-DO',self.browser.title)
        self.fail('Finish the test!')
    

if __name__ == '__main__':
    unittest.main(warnings='ignore')
