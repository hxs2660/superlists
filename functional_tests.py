#!/usr/bin/env python3
#codeing:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

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

    def check_for_row_in_list_table(self,row_text):
        table=self.browser.find_element_by_id('id_list_table')    
        rows=table.find_elements_by_tag_name('tr')
        self.assertIn(row_text,[row.text for row in rows])

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
        time.sleep(3)        
        self.check_for_row_in_list_table('1:Buy peacock feathers')
        #页面又显示了一个文本框，可以输入其他待办事项
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(3)
        #self.browser.implicitly_wait(10)
        self.check_for_row_in_list_table('1:Buy peacock feathers')
        self.check_for_row_in_list_table('2:Use peacock feathers to make a fly')
        #self.assertTrue(any(row.text=='1:Buy peacock feathers' for row in rows),
        #                "New to-do item did not appear in table --its text was:\n{}".format(table.text))

        self.fail('Finish the test!')
    

if __name__ == '__main__':
    unittest.main(warnings='ignore')
