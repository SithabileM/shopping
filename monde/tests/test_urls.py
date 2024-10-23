from django.test import SimpleTestCase
from django.urls import reverse,resolve
from monde.views import *

class TestUrls(SimpleTestCase):
    
        def test_index_url_is_resolved(self):
            url=reverse("index")
            self.assertEqual(resolve(url).func,index)
            
        def test_login_url_resolves(self):
            url=reverse("login")
            self.assertEqual(resolve(url).func,login_view)
            
        def test_submit_url_resolves(self):
            url=reverse("submit")
            self.assertEqual(resolve(url).func,submit)
            
        def test_logout_url_resolves(self):
            url=reverse("logout")
            self.assertEqual(resolve(url).func,logout_view)
            
        def test_submit_url_resolves(self):
            url=reverse("submit")
            self.assertEqual(resolve(url).func,submit)
            
        def test_sell_url_resolves(self):
            url=reverse("sell")
            self.assertEqual(resolve(url).func,sell_page)
            
        def test_cart_url_resolves(self):
            url=reverse("cart")
            self.assertEqual(resolve(url).func,add_to_cart)
            
        def test_single_url_resolves(self):
            url=reverse("single",args=[92])
            self.assertEqual(resolve(url).func,single_item)
            
        def test_restock_url_resolves(self):
            url=reverse("restock")
            self.assertEqual(resolve(url).func,restock)
            
        def test_remove_url_resolves(self):
            url=reverse("remove")
            self.assertEqual(resolve(url).func,remove_from_cart)
            
        def test_checkout_url_resolves(self):
            url=reverse("checkout")
            self.assertEqual(resolve(url).func,checkout)
            
        def test_addReview_url_resolves(self):
            url=reverse("addReview")
            self.assertEqual(resolve(url).func,review_view)
            
        def test_sellsManagement_url_resolves(self):
            url=reverse("sellsManagement")
            self.assertEqual(resolve(url).func,sellsManagement)
            
        def test_register_url_resolves(self):
            url=reverse("register")
            self.assertEqual(resolve(url).func,register)
            
        def test_deliver_url_resolves(self):
            url=reverse("deliver")
            self.assertEqual(resolve(url).func,deliver)
            
        
            
        