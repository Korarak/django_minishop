from . import views
from django.urls import path,include

urlpatterns = [
    path('',views.showproduct),
    path('login',views.login),
    path('register',views.register),
    path('logout',views.logout),
    path('myprofile',views.myprofile),
    path('editproduct',views.editproduct),
    path('addproduct',views.addproduct),
    path('search',views.search),
    path('cart',views.cart),
    path('addtocart/<int:id>',views.addtocart),
    path('editprofile/<int:id>',views.editprofile),
    path('checkout',views.checkout),
    path('showMyorder',views.showMyorder),
    path('del_cart_item/<int:id>',views.del_cart_item)
]