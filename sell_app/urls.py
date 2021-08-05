from . import views
from .views import CreatePost ,ProfileEditView, MyPost, DeleteProduct, ViewPurchase

from django.contrib.auth.views import LogoutView
from django.urls import (
    path,include
)

urlpatterns = [
    path('home/', views.home, name='home' ),
    path('', views.index, name='index' ),
    path('signup/', views.user_register, name='signup' ),
    path('product_desc/<int:pk>/', views.product_desc, name='product_desc' ),
    path('login',views.userlogin,name="login"),
    path('logout/',LogoutView.as_view(next_page='login'),name="logout"),
    path('token/', views.token_send, name='token' ),
    path('success/', views.success, name='success' ),
    path('verify/<auth_token>/', views.verify, name='verify' ),
    path('error/', views.error_page, name='error' ),
    path("accounts/", include("django.contrib.auth.urls")),
    path('create_post/', CreatePost.as_view(), name="create_post"),
    path('mypost/', MyPost.as_view(), name="mypost"),
    path('viewpurchase/', ViewPurchase.as_view(), name="viewpurchase"),
    
    path('show_product/', views.view_products, name="show_product"),
    path('product_details/', views.my_posts, name="product_details"),
    path('edit_post/<int:pk>', views.editpost, name="edit_post"),
    path('editprofile/', ProfileEditView.as_view(), name="editprofile"),
    path('viewbuyers/<int:pk>/', views.view_buyers, name="viewbuyers"),
    # path('buy/', BuyProduct.as_view(),name="buy"),
	path('accept/<int:pk>/',views.accept,name='accept'),
	path('sell/<int:pk>',views.send_email,name='send_mail'),
    path('deleteproduct/<int:pk>',DeleteProduct.as_view(),name='deleteproduct'),



   
]
