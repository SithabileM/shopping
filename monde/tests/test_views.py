from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from monde.models import *
import json
from monde.views import *

class TestViews(TestCase):
    def setUp(self):
        self.client=Client()
        self.factory=RequestFactory()
        self.item=ClothingItem.objects.create(
            id=2,
            name="coat",
            description="brown long coat",
            shortDescription="brown coat",
            rating=2,
            quantity=10,
            price=50,
            
        )
        
        self.user=User.objects.create_user(username='testuser',password="testpass")
        self.client.login(username='testuser',password='testpass')
        self.profile=UserProfile.objects.create(user=self.user,bank_balance=100)
        self.item2=ClothingItem.objects.create(id=3,name="shoe",image="shoe.jpg",price=20)
        self.cart_item=CartItems.objects.create(user=self.user,item=self.item2)
        
        
        
        
        self.index_url=reverse("index")
        self.register_url=reverse("register")
        self.login_url=reverse("login")
        self.logout_url=reverse("logout")
        self.sell_page_url=reverse("sell")
        self.single_item_url=reverse("single",args=[self.item.id])
        self.restock_url=reverse("restock")
        self.remove_url=reverse("remove")
        self.checkout_url=reverse("checkout")
        
        
    def test_index_GET(self):
        response=self.client.get(self.index_url,follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"monde/home.html")
        
    def test_register_GET(self):
        response=self.client.get(self.register_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, "monde/register.html")
        """
    def test_register_creates_user(self):
        response=self.client.post(self.register_url,{
        "username":"testUser",
        "password1":"strongpassword1234",
        "password2":"strongpassword1234"
        })
        self.assertEqual(response.status_code,200)
        self.assertTrue(User.objects.filter(Username='testUser').exists())
        """
    
    
        
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
    
    def test_single_item_view(self):
        response=self.client.get(self.single_item_url)
        self.assertIn("brown coat",response.content.decode())
        self.assertIn("brown long coat", response.content.decode())
        self.assertEqual(response.status_code,200)
   
    def test_restock_view_updates_quantity(self):
        original_quantity=self.item.quantity
        restock_amount=5
        response=self.client.post(self.restock_url,{
           "restock":restock_amount,
           "clothing_id":self.item.id
       })
        self.item.refresh_from_db()
        self.assertEqual(response.status_code,302)
        self.assertEqual(self.item.quantity,original_quantity+restock_amount)
        
    def test_remove_from_cart(self):
        self.client.login(username='testuser',password='testpass')
        
        response=self.client.post(self.remove_url,{'item': 'shoe.jpg'})
         
        self.assertRedirects(response,reverse('index'))  
        self.assertFalse(CartItems.objects.filter(user=self.user,item=self.item2).exists())
    
    def test_checkout_empty_cart(self):
        request=self.factory.get('/checkout/',{'subtotal':"Subtotal: $0"})
        request.user=self.user
        self.cart_item.delete()
        response=checkout(request)
        self.assertEqual(response.status_code,200)
        self.assertIn("Oops! It looks like your cart is empty",response.content.decode())
        
    def test_checkout_insufficient_balance(self):
        #Give the user a bank balance of 0
        self.profile.bank_balance=0
        self.profile.save()
        #Create a cart item
        item=CartItems.objects.create(user=self.user,item=self.item,amount=1)
        item.save()
        request=self.factory.get('/checkout/',{'subtotal':"Subtotal: $50"})
        request.user=self.user
        response=checkout(request)
        self.assertEqual(response.status_code,200)
        self.assertIn("Insufficient Balance",response.content.decode())
        
    def test_checkout_successful_checkout(self):
        item=CartItems.objects.create(user=self.user,item=self.item2,amount=1)
        item.save()
        request=self.factory.get('/checkout',{'subtotal':"Subtotal: $50"})
        request.user=self.user
        response=checkout(request)
        self.assertEqual(response.status_code,200)
        self.assertIn("Thank you for shopping with Monde :)", response.content.decode())
    