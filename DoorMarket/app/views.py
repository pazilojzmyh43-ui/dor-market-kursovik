"""
Контроллеры сайта DoorMarket.
Имена методов home, contact, about, links, registration, blog, blogpost, newpost
соответствуют лабораторным работам 1–6 и практическим занятиям.
"""
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db import models
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog
from .models import Comment
from .models import Category, Product, Order, OrderLine
from .forms import CommentForm
from .forms import BlogForm, CategoryForm, ProductForm


class RoleLoginView(LoginView):
    """Вход с переходом в раздел, который соответствует роли."""

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return '/users/'
        if user.is_staff:
            return '/orders/'
        return '/catalog/'


def _year():
    return datetime.now().year


def is_client(user):
    return user.is_authenticated and (not user.is_staff) and (not user.is_superuser)


def is_manager(user):
    return user.is_authenticated and user.is_staff and (not user.is_superuser)


def require_superuser(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_superuser:
        return redirect('home')
    return None


def require_client(request):
    if not is_client(request.user):
        return redirect('login')
    return None


def require_manager(request):
    if not is_manager(request.user):
        return redirect('login')
    return None


def get_cart(request):
    raw = request.session.get('cart', {})
    cart = {}
    for key, value in raw.items():
        try:
            cart[int(key)] = int(value)
        except (TypeError, ValueError):
            continue
    return cart


def save_cart(request, cart):
    request.session['cart'] = {str(key): qty for key, qty in cart.items() if qty > 0}
    request.session.modified = True


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.order_by('-posted')[:3]
    carousel_products = list(Product.objects.exclude(image='temp.jpg').order_by('id')[:6])
    categories = list(Category.objects.all().order_by('id')[:3])
    return render(
        request,
        'app/index.html',
        {
            'title': 'Главная',
            'posts': posts,
            'carousel_products': carousel_products,
            'categories': categories,
            'year': _year(),
        }
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Контакты',
            'message': 'Страница с нашими контактами.',
            'year': _year(),
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'О нас',
            'message': 'Сведение о нас',
            'year': _year(),
        }
    )


def links(request):
    """Renders the links page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title': 'Полезные ресурсы',
            'year': _year(),
        }
    )


def videopost(request):
    """Renders the video page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title': 'Видео',
            'year': _year(),
        }
    )


def blog(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.order_by('-posted')
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Новости',
            'posts': posts,
            'year': _year(),
        }
    )


def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=parametr)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            if not request.user.is_authenticated:
                return redirect('login')
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = Blog.objects.get(id=parametr)
            comment_f.save()
            return redirect('blogpost', parametr=post_1.id)
    else:
        form = CommentForm()
    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1,
            'comments': comments,
            'form': form,
            'year': _year(),
        }
    )


def newpost(request):
    """Renders the newpost page."""
    assert isinstance(request, HttpRequest)
    denied = require_superuser(request)
    if denied:
        return denied
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            post_f = form.save(commit=False)
            post_f.posted = datetime.now()
            post_f.author = request.user
            post_f.save()
            return redirect('blog')
    else:
        form = BlogForm()
    return render(
        request,
        'app/newpost.html',
        {
            'title': 'Добавление статьи',
            'form': form,
            'year': _year(),
        }
    )


def editpost(request, parametr):
    """Renders the edit post page."""
    assert isinstance(request, HttpRequest)
    denied = require_superuser(request)
    if denied:
        return denied
    post_1 = get_object_or_404(Blog, id=parametr)
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=post_1)
        if form.is_valid():
            form.save()
            return redirect('blogpost', parametr=post_1.id)
    else:
        form = BlogForm(instance=post_1)
    return render(
        request,
        'app/newpost.html',
        {
            'title': 'Редактирование статьи',
            'form': form,
            'year': _year(),
        }
    )


def deletepost(request, parametr):
    assert isinstance(request, HttpRequest)
    denied = require_superuser(request)
    if denied:
        return denied
    post_1 = get_object_or_404(Blog, id=parametr)
    if request.method == "POST":
        post_1.delete()
        return redirect('blog')
    return render(
        request,
        'app/confirm_delete.html',
        {
            'title': 'Удаление статьи',
            'object_name': post_1.title,
            'year': _year(),
        }
    )


def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()
            reg_f.save()
            return redirect('home')
    else:
        regform = UserCreationForm()
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,
            'year': _year(),
        }
    )


def catalog(request):
    """Renders the catalog page."""
    assert isinstance(request, HttpRequest)
    categories = Category.objects.all()
    return render(
        request,
        'app/catalog.html',
        {
            'title': 'Каталог',
            'categories': categories,
            'year': _year(),
        }
    )


def catalog_items(request, parametr):
    """Renders the category items page."""
    assert isinstance(request, HttpRequest)
    category = Category.objects.get(id=parametr)
    products = Product.objects.filter(category=category)
    return render(
        request,
        'app/catalog_items.html',
        {
            'title': category.name,
            'category': category,
            'products': products,
            'year': _year(),
        }
    )


def catalog_item(request, parametr):
    """Renders the catalog item page."""
    assert isinstance(request, HttpRequest)
    product = Product.objects.get(id=parametr)
    return render(
        request,
        'app/product.html',
        {
            'title': product.name,
            'product': product,
            'year': _year(),
        }
    )


def category_add(request):
    assert isinstance(request, HttpRequest)
    denied = require_superuser(request)
    if denied:
        return denied
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catalog')
    else:
        form = CategoryForm()
    return render(
        request,
        'app/category_form.html',
        {
            'title': 'Добавление категории',
            'form': form,
            'year': _year(),
        }
    )


def category_edit(request, parametr):
    assert isinstance(request, HttpRequest)
    denied = require_superuser(request)
    if denied:
        return denied
    category = get_object_or_404(Category, id=parametr)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('catalog_items', parametr=category.id)
    else:
        form = CategoryForm(instance=category)
    return render(
        request,
        'app/category_form.html',
        {
            'title': 'Редактирование категории',
            'form': form,
            'year': _year(),
        }
    )


def category_delete(request, parametr):
    assert isinstance(request, HttpRequest)
    denied = require_superuser(request)
    if denied:
        return denied
    category = get_object_or_404(Category, id=parametr)
    if request.method == "POST":
        category.delete()
        return redirect('catalog')
    return render(
        request,
        'app/confirm_delete.html',
        {
            'title': 'Удаление категории',
            'object_name': category.name,
            'year': _year(),
        }
    )


def product_add(request):
    assert isinstance(request, HttpRequest)
    denied = require_superuser(request)
    if denied:
        return denied
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog')
    else:
        form = ProductForm()
    return render(
        request,
        'app/product_form.html',
        {
            'title': 'Добавление товара',
            'form': form,
            'year': _year(),
        }
    )


def product_edit(request, parametr):
    assert isinstance(request, HttpRequest)
    denied = require_superuser(request)
    if denied:
        return denied
    product = get_object_or_404(Product, id=parametr)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('catalog_item', parametr=product.id)
    else:
        form = ProductForm(instance=product)
    return render(
        request,
        'app/product_form.html',
        {
            'title': 'Редактирование товара',
            'form': form,
            'year': _year(),
        }
    )


def product_delete(request, parametr):
    assert isinstance(request, HttpRequest)
    denied = require_superuser(request)
    if denied:
        return denied
    product = get_object_or_404(Product, id=parametr)
    if request.method == "POST":
        product.delete()
        return redirect('catalog')
    return render(
        request,
        'app/confirm_delete.html',
        {
            'title': 'Удаление товара',
            'object_name': product.name,
            'year': _year(),
        }
    )


def cart_add(request, parametr):
    assert isinstance(request, HttpRequest)
    denied = require_client(request)
    if denied:
        return denied
    product = get_object_or_404(Product, id=parametr)
    if request.method == "POST":
        cart = get_cart(request)
        cart[product.id] = cart.get(product.id, 0) + 1
        save_cart(request, cart)
    return redirect('cart')


def cart(request):
    """Renders the cart page."""
    assert isinstance(request, HttpRequest)
    denied = require_client(request)
    if denied:
        return denied
    cart_map = get_cart(request)
    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'update':
            for product_id in list(cart_map.keys()):
                raw = request.POST.get('qty_%s' % product_id)
                if raw is None:
                    continue
                try:
                    qty = int(raw)
                except ValueError:
                    qty = cart_map[product_id]
                if qty <= 0:
                    cart_map.pop(product_id, None)
                else:
                    cart_map[product_id] = min(qty, 99)
            save_cart(request, cart_map)
            return redirect('cart')
        if action == 'checkout':
            if cart_map:
                order = Order.objects.create(
                    client=request.user,
                    comment=request.POST.get('comment', ''),
                    status='new',
                    created=datetime.now(),
                )
                for product_id, qty in cart_map.items():
                    product = Product.objects.filter(id=product_id).first()
                    if product is None:
                        continue
                    OrderLine.objects.create(
                        order=order,
                        product=product,
                        name=product.name,
                        price=product.price,
                        quantity=qty,
                    )
                save_cart(request, {})
                return redirect('myorder', parametr=order.id)
            return redirect('cart')
    lines = []
    total = 0
    for product_id, qty in cart_map.items():
        product = Product.objects.filter(id=product_id).first()
        if product is None:
            continue
        line_sum = product.price * qty
        total += line_sum
        lines.append({'product': product, 'qty': qty, 'sum': line_sum})
    return render(
        request,
        'app/cart.html',
        {
            'title': 'Корзина',
            'lines': lines,
            'total': total,
            'year': _year(),
        }
    )


def myorders(request):
    """Renders the client orders page."""
    assert isinstance(request, HttpRequest)
    denied = require_client(request)
    if denied:
        return denied
    orders = Order.objects.filter(client=request.user).prefetch_related('lines')
    return render(
        request,
        'app/myorders.html',
        {
            'title': 'Мои заказы',
            'orders': orders,
            'year': _year(),
        }
    )


def myorder(request, parametr):
    assert isinstance(request, HttpRequest)
    denied = require_client(request)
    if denied:
        return denied
    order = get_object_or_404(Order, id=parametr, client=request.user)
    if request.method == "POST" and order.status == 'new':
        order.comment = request.POST.get('comment', '')
        order.save()
        for line in order.lines.all():
            raw = request.POST.get('qty_%s' % line.id)
            if raw is None:
                continue
            try:
                qty = int(raw)
            except ValueError:
                continue
            if qty <= 0:
                line.delete()
            else:
                line.quantity = min(qty, 99)
                line.save()
        return redirect('myorder', parametr=order.id)
    return render(
        request,
        'app/myorder.html',
        {
            'title': 'Заказ №%s' % order.id,
            'order': order,
            'year': _year(),
        }
    )


def myorder_delete(request, parametr):
    assert isinstance(request, HttpRequest)
    denied = require_client(request)
    if denied:
        return denied
    order = get_object_or_404(Order, id=parametr, client=request.user)
    if order.status != 'new':
        return redirect('myorders')
    if request.method == "POST":
        order.delete()
        return redirect('myorders')
    return render(
        request,
        'app/confirm_delete.html',
        {
            'title': 'Удаление заказа',
            'object_name': 'Заказ №%s' % order.id,
            'year': _year(),
        }
    )


def orders(request):
    """Renders the manager orders page."""
    assert isinstance(request, HttpRequest)
    denied = require_manager(request)
    if denied:
        return denied
    order_list = Order.objects.all().select_related('client').prefetch_related('lines')
    return render(
        request,
        'app/orders.html',
        {
            'title': 'Заказы',
            'orders': order_list,
            'year': _year(),
        }
    )


def order_manage(request, parametr):
    assert isinstance(request, HttpRequest)
    denied = require_manager(request)
    if denied:
        return denied
    order = get_object_or_404(Order, id=parametr)
    if request.method == "POST":
        status = request.POST.get('status')
        allowed = {code for code, _label in Order.STATUS_CHOICES}
        if status in allowed:
            order.status = status
            order.save()
        return redirect('order_manage', parametr=order.id)
    return render(
        request,
        'app/order_manage.html',
        {
            'title': 'Заказ №%s' % order.id,
            'order': order,
            'statuses': Order.STATUS_CHOICES,
            'year': _year(),
        }
    )


def users(request):
    assert isinstance(request, HttpRequest)
    denied = require_superuser(request)
    if denied:
        return denied
    accounts = User.objects.filter(is_superuser=False).order_by('username')
    return render(
        request,
        'app/users.html',
        {
            'title': 'Пользователи',
            'accounts': accounts,
            'year': _year(),
        }
    )


def manager_add(request):
    """Регистрация пользователя с ролью «Менеджер»."""
    assert isinstance(request, HttpRequest)
    denied = require_superuser(request)
    if denied:
        return denied
    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = True
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()
            reg_f.first_name = request.POST.get('first_name', '')
            reg_f.last_name = request.POST.get('last_name', '')
            reg_f.save()
            return redirect('users')
    else:
        regform = UserCreationForm()
    return render(
        request,
        'app/manager_add.html',
        {
            'title': 'Регистрация менеджера',
            'regform': regform,
            'year': _year(),
        }
    )


def user_delete(request, parametr):
    assert isinstance(request, HttpRequest)
    denied = require_superuser(request)
    if denied:
        return denied
    account = get_object_or_404(User, id=parametr)
    if account.is_superuser or account.id == request.user.id:
        return redirect('users')
    if request.method == "POST":
        account.delete()
        return redirect('users')
    return render(
        request,
        'app/confirm_delete.html',
        {
            'title': 'Удаление пользователя',
            'object_name': account.username,
            'year': _year(),
        }
    )
