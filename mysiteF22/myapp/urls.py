from django.urls import path
#from myapp import views

#from myapp import myapp
from . import views
from django.urls import include

app_name = 'myapp'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about/', views.about, name='about'),
    path(r'<int:cat_no>/', views.detail, name='detail'),
    path(r'products/', views.products, name='products'),
    path(r'placeorder/', views.place_order, name='placeorder'),
    path(r'products/<int:prod_id>/', views.product_detail, name='product_detail'),
    path(r'login/',views.user_login, name='login'),
    path(r'logout/',views.user_logout, name='logout'),
    path(r'myorders/',views.myorders, name='myorders'),
    path(r'register/', views.user_register, name='register'),
    path(r'forget_password/', views.forget_password, name='forget_password')

]
