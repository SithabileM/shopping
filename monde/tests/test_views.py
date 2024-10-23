from django.test import TestCase, Client
from django.urls import reverse
from monde.models import *
import json

class TestViews(TestCase):
    def setUp(self):
        self.client=Client()
        self.index_url=reverse("index")
        self.register_url=reverse("register")
        self.login_url=reverse("login")
        self.logout_url=reverse("logout")
        self.sell_page_url=reverse("sell")
        
    def test_index_GET(self):
        response=self.client.get(self.index_url,follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"monde/login.html")
        
    def test_register_GET(self):
        response=self.client.get(self.register_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, "monde/register.html")
        
    #test login
    def test_login_view_GET(self):
        response=self.client.get(self.login_url,follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"monde/login.html")
        
    #test logout
    
    def test_logout_view_GET(self):
        response=self.client.get(self.logout_url,follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"monde/login.html")
        
    def test_sell_page_GET(self):
        response=self.client.get(self.sell_page_url,follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"monde/sell.html")
        
    
        
    