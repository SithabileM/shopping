from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path("login/",views.login_view,name="login"),
    path("logout/",views.logout_view, name="logout"),
    path("submit/",views.submit,name="submit"),
    path("sell/",views.sell_page,name='sell'),
    path("cart",views.add_to_cart,name="cart"),
    path("<int:clothing_id>", views.single_item,name="single"),
    path("restock",views.restock,name="restock"),
    path("remove",views.remove_from_cart,name="remove"),
    path("checkout",views.checkout,name="checkout"),
    path("addReview",views.review_view,name="addReview"),
    path("sellsManagement",views.sellsManagement,name="sellsManagement"),
    path("register",views.register,name="register")
]