"""taskproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from resturaant import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homepage),
    path('<slug:food_category>',views.homepage),
    path('register/', views.register),
    path('login/', views.user_login),
    path('logout/', views.user_logout),
    path('item/<str:food_item>/', views.item_view),
    path('cart/', views.cart_view),
    path('cart/<slug:coupon>', views.cart_view),
    path('empty/cart',views.empty_cart),
    path('addresses/',views.addresses),
    path('previous/order',views.previous_order),
    path('feedback/<int:id>',views.feedback),
    path('create_coupons/', views.create_coupon),
    path('view/coupons', views.view_coupons),
    path('premium/', views.go_premium),
    path('view/meal', views.view_meal),
    path('add/meal/<int:id>', views.add_meal),
    path('create/meal', views.create_meal),
    path('meal/<int:id>', views.add_meal_item),
    path('item/remove/<int:id>', views.remove_meal_item),
    path('filter/price',views.filter_price),
    path('search/item',views.search_bar)
]
