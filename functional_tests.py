#!/usr/bin/env python3
#codeing:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):
    """docstring for NewVisittorTest"""
    #测试之前运行
    def setUp(self):
        #self.browser=webdriver.Firefox()
        self.browser=webdriver.PhantomJS(executable_path='../phantomjs')
        self.browser.implicitly_wait(3)

    #测试之后运行    
    def tearDown(self):
        self.browser.quit()

    #测试方法    
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        #self.browser.get('http://blog.hehome.top')
        self.assertIn('To-Do',self.browser.title)
        header_text=self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)
        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                        inputbox.get_attribute('placeholder'),
                        'Enter a to-do item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        table=self.browser.find_element_by_id('id_list_table')
        rows=table.find_elements_by_tag_name('tr')
        self.assertTrue(any(row.text=='1:Buy peacock feathers' for row in rows))

        self.fail('Finish the test!')
    

if __name__ == '__main__':
    unittest.main(warnings='ignore')
