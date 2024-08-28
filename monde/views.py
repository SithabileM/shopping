from django.shortcuts import render,HttpResponseRedirect,redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .models import ClothingItem,UserProfile,CartItems,Sections,UserOwnedItems,Review
from .form import ClothingForm
from datetime import date

def search(searchTerm):
    """generate sections and the data for each section"""
    sections=Sections.objects.all()
    sectionData={}
    for section in sections:
        #Get the section Id
        sectionId=section.id
        sectionItems=ClothingItem.objects.filter(clothingSections=sectionId,description__icontains=searchTerm)
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
                self.cart_data[str(currentImg)]=(["Amount in cart: "+str(amnt),"Price: $"+ str(prc)])
        return self.cart_data
    def deleteCart(self,user):
        self.items=CartItems.objects.filter(user=user)
        for i in self.items:
            i.delete()
        self.cart_data={}
              
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
    return render(request,"monde/logout.html")

def submit(request):
    return render(request,"monde/home.html")

def sell_page(request):
    year=date.today().year
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
        image=request.POST["image"]
        
        current = ClothingItem.objects.create(name=name)
        current.description=description
        current.shortDescription=shortDescription
        current.quantity=quantity
        current.price=price
        current.image="images/"+str(year)[-2:]+"/"+image
        current.save()
        
    return(render(request,"monde/sell.html",{
        "sections":sections,
    }))

def single_item(request,clothing_id):
    clothing_id=str(clothing_id).replace("{%url ","")
    clothing_id=clothing_id.replace("}","")
    items=ClothingItem.objects.all()
    
    #determine whether the current user is the seller of the item
    isSeller=None
    for item in items:
        if item.id == int(clothing_id):
            #Determine whether the currently selected item was sold by currently logged in user
            isSeller=UserProfile.objects.filter(user=request.user,inventory=item)
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
                "image":item.image,
                "clothing_id":clothing_id,
                "isSeller":isSeller,
                "reviews":reviews
                
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
def remove_from_cart(request):
    #get the key of the item to be removed
    myItem=request.GET.get("item")
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
    #add them to the user owned items
    for i in cartItems.keys():
        myItem=ClothingItem.objects.get(image=i)
        UserOwnedItems.objects.create(clothing_item=myItem,user=request.user)
    #decrease the users balance by the subtotal
    user.bank_balance=balance-subtotal
    user.save()
    #Increase the sellers bank account of each item by the subtotal
    for i in cartItems.keys():
        #looking for the name of an item in clothingItems with an image(i)
        item=ClothingItem.objects.get(image=i)
        myItem=item.id
        #check who is the seller by finding out who has the item in the inventory
        isSeller=UserProfile.objects.get(inventory=myItem)
        isSeller.bank_balance += subtotal
        isSeller.save()
        
    #decrease the quentity of clothing items
    
    #clear the users cart
    cart.deleteCart(request.user)
    #display a success message
    return HttpResponse("Thank You for shopping with Monde :)")

def review_view(request):
    """Get a review from the items page and put it up in the admin page"""
    if request.method=="POST":
        userReview=request.POST["userReview"]
        clothing=int(request.POST['clothing'])
        print(userReview)
        print(clothing)
    Review.objects.create(user=request.user, reviewItem=clothing,review=userReview)
    return HttpResponseRedirect("single")

def sellsManagement(request):
    
    myUser=UserProfile.objects.get(user=request.user.id)
    inventory=myUser.inventory.all()
    
    tableContent={}
    Deliveries=set()
    for i in inventory:
        items=UserOwnedItems.objects.filter(clothing_item=i)
        for j in items:
            clothingId=j.clothing_item.id
            if j.status is False:
                status="Pending..."
            else:
                status="Delivered"
            Deliveries.add("Deliver item " + str(clothingId))
            tableContent[j.user]=[str(j.clothing_item),str(clothingId),str(status)]
            

            
    return render(request,"monde/sellsManagement.html",{
       "sellsTableContent":tableContent,
       "DeliveriesButtonsContent": Deliveries
    })