"""Маршруты проекта DoorMarket. Файл urls.py шаблона Visual Studio 2019."""
from datetime import datetime
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from app import forms, views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('links/', views.links, name='links'),
    path('blog/', views.blog, name='blog'),
    path('blogpost/<int:parametr>/', views.blogpost, name='blogpost'),
    path('newpost/', views.newpost, name='newpost'),
    path('newpost/<int:parametr>/', views.editpost, name='editpost'),
    path('newpost/<int:parametr>/delete/', views.deletepost, name='deletepost'),
    path('videopost/', views.videopost, name='videopost'),
    path('registration/', views.registration, name='registration'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/items/<int:parametr>/', views.catalog_items, name='catalog_items'),
    path('catalog/item/<int:parametr>/', views.catalog_item, name='catalog_item'),
    path('catalog/category/add/', views.category_add, name='category_add'),
    path('catalog/category/<int:parametr>/edit/', views.category_edit, name='category_edit'),
    path('catalog/category/<int:parametr>/delete/', views.category_delete, name='category_delete'),
    path('catalog/product/add/', views.product_add, name='product_add'),
    path('catalog/product/<int:parametr>/edit/', views.product_edit, name='product_edit'),
    path('catalog/product/<int:parametr>/delete/', views.product_delete, name='product_delete'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:parametr>/', views.cart_add, name='cart_add'),
    path('myorders/', views.myorders, name='myorders'),
    path('myorders/<int:parametr>/', views.myorder, name='myorder'),
    path('myorders/<int:parametr>/delete/', views.myorder_delete, name='myorder_delete'),
    path('orders/', views.orders, name='orders'),
    path('orders/<int:parametr>/', views.order_manage, name='order_manage'),
    path('users/', views.users, name='users'),
    path('users/manager/', views.manager_add, name='manager_add'),
    path('users/<int:parametr>/delete/', views.user_delete, name='user_delete'),
    path('login/',
         views.RoleLoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Вход',
                 'year': datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
