from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name="start"),
    path('dashboard/', views.dashboard, name="affiliate_dashboard"),
    path('customer_orders/', views.customer_orders, name="customer_orders"),
    path('billing/', views.billing, name="billing"),
    path('add_billing/', views.add_billing, name="add_billing"),
    path('signup/', views.signup, name='affiliate-signup'),
    path('login/', views.loginn, name='affiliate-login'),
    path('logout/', views.logout_v, name='affiliate-logout'),
    
]
