#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
#from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import  sys

class NewVisitorTest(StaticLiveServerTestCase):
    """docstring for NewVisittorTest"""
    #临时服务器地址
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url='http://'+arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url=cls.live_server_url
    @classmethod
    def tearDownClass(cls):
        if cls.server_url==cls.live_server_url:
            super().tearDownClass()

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

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)
        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width']/2,512,delta=5
            )
        inputbox.send_keys('testing\n')
        time.sleep(1)
        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width']/2,512,delta=5
            )
       

    #测试方法    
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)
        #self.browser.get('http://blog.hehome.top')
        self.assertIn('To-Do',self.browser.title)
        header_text=self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)
        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                        inputbox.get_attribute('placeholder'),
                        'Enter a to-do item')
        #edith输入了一个新待办事项，新建了一个清单
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        #edith获得了他的唯一URL 
        edith_list_url=self.browser.current_url
        self.assertRegex(edith_list_url,'/lists/.+')        
        self.check_for_row_in_list_table('1:Buy peacock feathers')
        #页面又显示了一个文本框，可以输入其他待办事项
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        #检查两次输入清单是否已经保存
        self.check_for_row_in_list_table('1:Buy peacock feathers')
        self.check_for_row_in_list_table('2:Use peacock feathers to make a fly')
        
        #使用一个新浏览器会话
        self.browser.quit()
        self.setUp()

        #首页看不到上面的清单
        self.browser.get(self.live_server_url)
        page_text=self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertNotIn('make a fly',page_text)

        #francis输入了一个新待办事项，新建了一个清单
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        #francis获得了他的唯一URL
        francis_list_url=self.browser.current_url
        self.assertRegex(francis_list_url,'/lists/.+')
        self.assertNotEqual(francis_list_url,edith_list_url)

        #self.fail('Finish the test!')
    
