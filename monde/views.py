from django.shortcuts import render,HttpResponseRedirect,redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .models import *
from .form import ClothingForm
from datetime import date
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.views.decorators.http import require_POST
from imagekitio import ImageKit
import os
from django.conf import settings

def search(searchTerm):
    """generate sections and the data for each section"""
    sections=Sections.objects.all()
    sectionData={}
    for section in sections:
        #Get the section Id
        sectionId=section.id
        sectionItems=ClothingItem.objects.filter(Q(description__icontains=searchTerm)|Q(shortDescription__icontains=searchTerm),clothingSections=sectionId,)
        sectionData[section.name]=sectionItems
        
    return sectionData
    
def get_sections():
    """generate sections and the data for each section"""
    sections=Sections.objects.all()
    sectionData={}
    for section in sections:
        #Get the section Id
        sectionId=section.id
        sectionItems=ClothingItem.objects.filter(clothingSections=sectionId)
        sectionData[section.name]=sectionItems
    return sectionData
         
#gets the contents of the users cart 
class MyCart:
    def __init__(self):
        self.cart_data={}
    def getCart(self,user):
        self.items=CartItems.objects.filter(user=user)
        for i in self.items:
        #check if child object is not none
            if i.item is not None:
                currentImg=i.item.image
                amnt=i.amount
                prc=i.item.price
                self.cart_data[str(currentImg)]=([str(amnt),str(prc)])
        return self.cart_data
    
    
    def deleteCart(self,user):
        self.items=CartItems.objects.filter(user=user)
        for i in self.items:
            i.delete()
            i.save()
        self.cart_data={}
        return
        
def register(request) :
    form=UserCreationForm()
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context={"form":form}
    return render(request,"monde/register.html",context)
           
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return (HttpResponseRedirect("login"))
    #get the item names and images and prices in the cart of currently signed in user
    user=request.user
    cart_data={}
    items=CartItems.objects.filter(user=user)
    #generate a subtotal for the users cart
    subtotal=0
    #add to a dictionary variable, the users cart information from the cart items model
    for i in items:
        #check if child object is not none
        if i.item is not None:
            amnt=i.amount
            subtotal=subtotal+i.item.price*amnt
        elif i.item is None:
            continue 
    cart=MyCart()
    cart_data=cart.getCart(request.user)
        
    #get the data when a user attempts to sell an item, so that it can be displayed on home page
    if request.method=="POST":
        form=ClothingForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            obj=form.instance
            return render(request,'monde/home.html',{"obj":obj})
    else:
        #If there is no new clothing item submitted return the form with the existing items
        form=ClothingForm()
        
    img=ClothingItem.objects.all()
    sectionData=get_sections()
    if request.method=="POST":
        searchTerm=request.POST["search"]
        sectionData=search(searchTerm)
         
    return render(request,"monde/home.html",{
        "sectionData": sectionData,
        "img":img,
        "form":form,
        #variables that store data used to load cart
        "cart_data":cart_data,
        "subtotal":"Subtotal: $"+str(subtotal)
        })
         
def login_view(request):
    if request.method=="POST":
        password= request.POST["password"]
        username=request.POST["username"]
        user=authenticate(request,password=password, username=username)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
    return(render(request,"monde/login.html"))

def logout_view(request):
    logout(request)
    return redirect("login")

def submit(request):
    return render(request,"monde/home.html")

def sell_page(request):
    
    imagekit = ImageKit(
    private_key= settings.IMAGEKIT_PRIVATE_KEY,
    public_key=settings.IMAGEKIT_PUBLIC_KEY,
    url_endpoint=settings.IMAGEKIT_URL_ENDPOINT
)
    
    sectionData=get_sections()
    sections=[]
    
    for i,v in sectionData.items():
        sections+=[i]
    if request.method=="POST":
        name=request.POST["name"]
        description=request.POST["description"]
        shortDescription=request.POST["shortDescription"]
        quantity=request.POST["quantity"]
        price=request.POST["price"]
        image=request.FILES["image"]
        sections=request.POST.getlist("sections")
        upload= imagekit.upload_file(
            file=image,
            file_name=image.name,
        )
        
        image_url = upload["response"]["url"]

        current = ClothingItem.objects.create(name=name)
        current.description=description
        current.shortDescription=shortDescription
        current.quantity=quantity
        current.price=price
        current.image=image
        current.image_url=image_url
        for i in sections:
            sec=Sections.objects.get(name=i)
            secId=sec.id
            current.clothingSections.add(secId)
        current.save()
        
        #add the item to inventory
        user=UserProfile.objects.get(user=request.user)
        user.inventory.add(current.id)
        user.save()
        
    return(render(request,"monde/sell.html",{
        "sections":sections,
    }))

def single_item(request,clothing_id):
    clothing_id=str(clothing_id).replace("{%url ","")
    clothing_id=clothing_id.replace("}","")
    items=ClothingItem.objects.all()
    
    #determine whether the current user is the seller of the item
    isSeller=False
    for item in items:
        if item.id == int(clothing_id):
            #Determine whether the currently selected item was sold by currently logged in user
            isSeller=UserProfile.objects.filter(user=request.user.id,inventory=item)
            if isSeller:
                isSeller=True
            #get all reviews
            reviews=Review.objects.filter(reviewItem=int(clothing_id))
            return render(request,"monde/single.html",{
                "description":item.description,
                "shortDescription":item.shortDescription,
                "name":item.name,
                "rating":item.rating,
                "quantity":item.quantity,
                "price":item.price,
                "image":item.image_url,
                "clothing_id":clothing_id,
                "isSeller":isSeller,
                "reviews":reviews,
                "shippingDate": item.shippingDate
                
            })
    return HttpResponse()

def add_to_cart(request):
    clothing_id=request.GET.get("clothing_id")
    amount=request.GET.get("amount")
    currentUser,created=CartItems.objects.get_or_create(user=request.user,item_id=clothing_id,amount=amount)
    if not created:
        currentUser.amount+=1
    currentUser.save()
    return redirect("index")
    
#lets the user restock items they have sold
def restock(request):
    amount=request.POST["restock"]
    #get the clothing id of the item
    imageId=request.POST.get("clothing_id")
    #get the existing quantity and add the amount you want to add
    item=ClothingItem.objects.get(id=imageId)
    itemQuantity=item.quantity
    #find the items field and update the quantity
    newQuantity=itemQuantity+int(amount)
    item.quantity=newQuantity
    item.save()
    return redirect("index")

#remove an item from the current users cart
@require_POST
def remove_from_cart(request):
    #get the key of the item to be removed
    myItem=request.POST.get("item")
    cart=CartItems.objects.filter(user=request.user)
    for i in cart:
        #check if child object is not none
        if i.item is not None:
            if i.item.image==myItem:
                i.delete()
    return redirect("index")

#peforms necessary operations for the checkout process
def checkout(request):
    #get the subtotal
    subtotal=request.GET.get("subtotal")
    #check if user has a sufficcient balance for the purchase and if not, display a message
    subtotal=float(subtotal[11:])
    user=UserProfile.objects.get(user=request.user.id)
    balance=user.bank_balance
    if balance < subtotal:
        return HttpResponse("Insufficient Balance: You have insufficient funds to proceed with the payments")
    #get the submitted cart items
    cart=MyCart()
    cartItems=cart.getCart(request.user)
    for i in cartItems:
        #decrease each items quantity
        itemToDecrease=ClothingItem.objects.get(image=i)
        itemToDecrease.quantity-=int(cartItems[i][0])
        itemToDecrease.save()
        #decrease the current users bank balance by the amount
        user=UserProfile.objects.get(user=request.user)
        user.bank_balance -= float(cartItems[i][1])
        #increase the seller of i bank balance by the price
        itemToDecreaseId=itemToDecrease.id
        seller=UserProfile.objects.get(inventory=itemToDecreaseId)
        seller.bank_balance+=float(cartItems[i][1])
        seller.save()
        #make the item a user owned item
        UserOwnedItems.objects.create(
            user=request.user,
            clothing_item=itemToDecrease,
            amount_purchased=int(cartItems[i][0]),
            status=False
            )
    #clear the users cart
    if not cartItems:
        return HttpResponse("Oops! It looks like your cart is empty")
    myCart=CartItems.objects.filter(user=request.user)
    for item in myCart:
        item.delete()
    #display a success message
    cartItems={}
    return HttpResponse("Thank You for shopping with Monde :)")

def review_view(request):
    """Get a review from the items page and put it up in the admin page"""
    currentUser=request.user
    if request.method=="POST":
        userReview=request.POST["userReview"]
        clothing=int(request.POST['clothing'])
        clothingInst=ClothingItem.objects.get(id=clothing)
    if userReview != "":
        Review.objects.create(user=currentUser, reviewItem=clothingInst,review=userReview)
    return HttpResponseRedirect("/monde/"+str(clothing))
   

def sellsManagement(request):
    myUser=UserProfile.objects.get(user=request.user.id)
    inventory=myUser.inventory.all()
    tableContent={}
    Deliveries=set()
    TotalAmount={}
    for i in inventory:
        items=UserOwnedItems.objects.filter(clothing_item=i)
        for j in items:
            clothingId=j.clothing_item.id
            TotalAmount[clothingId]= j.clothing_item.price*j.clothing_item.quantity
            if j.status is False:
                status="Pending..."
                Deliveries.add(str(clothingId))
                tableContent[str(clothingId) + str(j.user)]=[str(j.user),str(j.clothing_item),str(clothingId),str(status), str(j.amount_purchased)]
                    
            else:
                status="Delivered"
          
    return render(request,"monde/sellsManagement.html",{
       "sellsTableContent":tableContent,
       "DeliveriesButtonsContent": Deliveries,
    })
    
def deliver(request):
    item=request.GET.get("item")
    itemsToDeliver=UserOwnedItems.objects.filter(clothing_item=int(item), status=False)
    #set status to True
    for item in itemsToDeliver:
        item.status=True
        item.save()
    return HttpResponse()
