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
        
        self.inventoryItem1=ClothingItem.objects.create(
            id=4,
            name="cup",
            description="fancy pink cup",
            shortDescription="fancy cup",
            quantity=10,
            price=5,
        )
        self.inventoryItem2=ClothingItem.objects.create(
            id=5,
            name="item2",
            description="electric purple blankets",
            shortDescription="blankets",
            quantity=40,
            price=150,
        )
        self.inventoryItem3=ClothingItem.objects.create(
            id=6,
            name="Item3",
            description="soft 2 designs duvets",
            shortDescription="duvets",
            quantity=30,
            price=30,
        )
        
        self.user=User.objects.create_user(username='testuser',password="testpass")
        self.client.login(username='testuser',password='testpass')
        self.profile=UserProfile.objects.create(user=self.user,bank_balance=100)
        self.profile.inventory.add(4,5,6)
        self.profile.save()
        self.item2=ClothingItem.objects.create(id=3,name="shoe",image="shoe.jpg",price=20)
        self.cart_item=CartItems.objects.create(user=self.user,item=self.item2)
        self.user2=User.objects.create_user(username='testuser2',password="testpass2")
        self.user3=User.objects.create_user(username='testuser3',password="testpass3")
        
        self.index_url=reverse("index")
        self.register_url=reverse("register")
        self.login_url=reverse("login")
        self.logout_url=reverse("logout")
        self.sell_page_url=reverse("sell")
        self.single_item_url=reverse("single",args=[self.item.id])
        self.restock_url=reverse("restock")
        self.remove_url=reverse("remove")
        self.checkout_url=reverse("checkout")
        self.sellsManagement_url=reverse("sellsManagement")
           
    def test_index_GET(self):
        response=self.client.get(self.index_url,follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"monde/home.html")
        
    def test_register_GET(self):
        response=self.client.get(self.register_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, "monde/register.html")
        
    def test_register_creates_user(self):
        response=self.client.post(self.register_url,{
        "username":"RegisteredUser",
        "password1":"strongpassword1234",
        "password2":"strongpassword1234"
        })
        self.assertEqual(response.status_code,302)
        self.assertTrue(User.objects.filter(username='RegisteredUser').exists())
        
    
    
        
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
        
    def test_sellsManagement_get(self):
        self.client.login(username='testuser',password='testpass')
        ownedItem1=UserOwnedItems.objects.create(user=self.user2,clothing_item=self.inventoryItem1,amount_purchased=3)
        ownedItem2=UserOwnedItems.objects.create(user=self.user3,clothing_item=self.inventoryItem1,amount_purchased=4)
        ownedItem1.save()
        ownedItem2.save()
        response=self.client.get(self.sellsManagement_url)
        self.assertIn(self.user2.username,response.content.decode())
        self.assertIn(self.user3.username,response.content.decode())
        self.assertIn("3",response.content.decode())
        self.assertIn("4",response.content.decode())
        self.assertIn(str(self.inventoryItem1.pk),response.content.decode())
        self.assertEqual(response.status_code,200)
        
    def test_review_view_review(self):
        self.client.force_login(self.user)
        #Post a review and display on page
        request=self.factory.post('/addReview/',{'userReview':"Excellent cup!", 'clothing':"6"})
        request.user=self.user
        response=review_view(request)
        self.assertEqual(response.status_code,302)
        
    def test_deliver_view(self):
        request=self.factory.get('/deliver/',{"item":"4"})
        response=deliver(request)
        self.assertEqual(response.status_code,200)
        item1=UserOwnedItems.objects.filter(user=self.user2,clothing_item=self.inventoryItem1,amount_purchased=3)
        item2=UserOwnedItems.objects.filter(user=self.user3,clothing_item=self.inventoryItem1,amount_purchased=4)
        self.assertFalse(item1.exists())
        self.assertFalse(item2.exists())
        self.assertEqual(response.status_code,200)
        
class CheckoutTestCase(TestCase):
    def setUp(self):
        self.client=Client()
        self.user=User.objects.create_user(username='testuser',password='pass1234')
        self.user_profile=UserProfile.objects.create(user=self.user,bank_balance=200)
        self.client.login(username='testuser',password='pass1234')
        self.seller_user=User.objects.create_user(username='seller',password='pass1234')
        self.seller_profile=UserProfile.objects.create(user=self.seller_user,bank_balance=0)
        self.item=ClothingItem.objects.create(name='TestShirt',price=100,quantity=10,seller=self.seller_profile) 
        CartItems.objects.create(user=self.user,clothing_item=self.item,quantity=1)
        
    def checkout_success(self):
        response=self.client.get('/checkout/')
        self.assertEqual(response.status_code,200)
        self.assertIn('Thank you for shopping',response.content.decode())
        self.seller_profile.refresh_from_db()
        self.user_profile.refresh_from_db()
        self.assertEqual(self.seller_profile.bank_balance,100)  
        self.assertEqual(self.user_profile.bank_balance,100)  
        self.assertTrue(UserOwnedItems.objects.filter(user=self.user,clothing_item=self.item).exists())
        self.assertFalse(CartItems.objects.filter(user=self.user).exists())   
