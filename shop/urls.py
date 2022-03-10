from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('product/<slug:slug>/', views.product_page , name="product-page"),
    path('category/<slug:category>/', views.category , name="category"),
    path('all_products/', views.all_products , name="all_products"),

    path('add_coupon/', views.add_coupon, name='add_coupon'),
    path('delete_item/', views.delete_item, name='delete_item'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),

    path('mycart/', views.mycart, name='mycart'),
    path('add_order/', views.add_order, name='add_order'),

    
    path('action_plus/<str:id>/', views.action_plus, name='action_plus'),
    path('action_minus/<str:id>/', views.action_minus, name='action_minus'),

    path('checkout/', views.checkout , name='checkout'),
    path('delete_address/<int:id>/', views.delete_address, name='delete_address'),
    path('activate_address/<int:id>/', views.activate_address, name='activate_address'),
    path('add_address/', views.add_address, name='add_address'),

    
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('about-us/', views.about_us, name='about_us'),

]
