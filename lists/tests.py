from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item,List

class HomePageTest(TestCase):
    #测试主页解析
    def test_root_url_resolve_to_home_page_view(self):
        found=resolve('/')
        self.assertEqual(found.func,home_page)
    #返回正确首页
    def test_home_page_returns_correct_html(self):
        request=HttpRequest()
        response=home_page(request)
        expected_html=render_to_string('home.html')
        #print(expected_html)
        self.assertEqual(response.content.decode(),expected_html)
    #测试保存POST请求    
    def test_home_page_can_save_a_POST_request(self):
        request=HttpRequest()
        request.method='POST'
        request.POST['item_text']='A new list item'

        response=home_page(request)
        self.assertEqual(Item.objects.count(),1)
        new_item=Item.objects.first()
        self.assertEqual(new_item.text,'A new list item')

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list=List.objects.create()
        correct_list=List.objects.create()

        self.client.post(
            '/lists/{}/add_item'.format(correct_list.id), 
            data={'item_text':'A new list item'}
            )
        self.assertEqual(Item.objects.count(),1)

        new_item=Item.objects.first()
        self.assertEqual(new_item.text,'A new list item')
        self.assertEqual(new_item.list,correct_list)

    def test_redirects_to_list_view(self):
        other_list=List.objects.create()
        correct_list=List.objects.create()

        response=self.client.post(
            '/lists/{}/add_item'.format(correct_list.id), 
            data={'item_text':'A new list item'}
            )
        self.assertRedirects(response,'/lists/{}/'.format(correct_list.id))

    #首页POST之后重定向    
    def test_home_page_redirects_after_POST(self):
        request=HttpRequest()
        request.method='POST'
        request.POST['item_text']='A new list item'
        
        response=home_page(request)
        new_list=List.objects.first()
        self.assertEqual(response.status_code,302)
        self.assertEqual(response['location'],'/lists/{}/'.format(new_list.id))
    
    def test_redirects_after_POST(self):
        response=self.client.post(
            '/lists/new',
            data={'item_text':'A new list item'}
            )
        new_list=List.objects.first()
        self.assertRedirects(response,'/lists/{}/'.format(new_list.id))

class ListAndItemModelsTest(TestCase):
    #保存、读出
    def test_saving_and_retrieving_items(self):
        list_=List()
        list_.save()

        first_item=Item()
        first_item.text='The first (ever) list item'
        first_item.list=list_
        first_item.save()

        second_item=Item()
        second_item.text='Item the second'
        second_item.list=list_
        second_item.save()       

        saved_list=List.objects.first()
        self.assertEqual(saved_list,list_)

        saved_items=Item.objects.all()
        self.assertEqual(saved_items.count(),2)



        first_saved_item=saved_items[0]
        second_saved_item=saved_items[1]
        self.assertEqual(first_saved_item.text,'The first (ever) list item')
        self.assertEqual(first_saved_item.list,list_)        
        self.assertEqual(second_saved_item.text,'Item the second')
        self.assertEqual(second_saved_item.list,list_) 

class ListViewTest(TestCase):
    #测试使用模版
    def test_uses_list_Template(self):
        list_=List.objects.create()
        response=self.client.get('/lists/{}/'.format(list_.id))
        self.assertTemplateUsed(response,'list.html')

    def test_passes_correct_list_to_template(self):
        other_list=List.objects.create()
        correct_list=List.objects.create()
        response=self.client.get('/lists/{}/'.format(correct_list.id))
        self.assertEqual(response.context['list'],correct_list)

    #主页显示清单 
    def test_displays_only_items_for_that_list(self):
        correct_list=List.objects.create()
        Item.objects.create(text='itemey 1',list=correct_list)
        Item.objects.create(text='itemey 2',list=correct_list)
        other_list=List.objects.create()
        Item.objects.create(text='other list itemey 1',list=other_list)
        Item.objects.create(text='other list itemey 2',list=other_list)  
        response=self.client.get('/lists/{}/'.format(correct_list.id))
        self.assertContains(response,'itemey 1')
        self.assertContains(response,'itemey 2')
        self.assertNotContains(response,'other list itemey 1')
        self.assertNotContains(response,'other list itemey 2')