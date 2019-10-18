from django.shortcuts import render
from shop.models import Category, Product, CartItem, Cart, Order, Comment
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from decimal import Decimal
from shop.forms import OrderForm, RegistrationForm, LoginForm, CommentForm
from django.contrib.auth import login, authenticate
from sklearn.linear_model import LinearRegression


def base_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products,
        'cart': cart,
    }
    return render(request, 'base.html', context)


def product_view(request, product_slug):

    x = []
    y = []
    for product in Product.objects.all():
        x.append([product.processor, product.ozu])
        y.append(product.price)
    model = LinearRegression().fit(x, y)

    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product = Product.objects.get(slug=product_slug)

    product.predicted_price = model.predict([[product.processor, product.ozu]])

    categories = Category.objects.all()

    context = {
        'product': product,
        'categories':categories,
        'cart': cart
    }
    return render(request, 'product.html', context)


def category_view(request, category_slug):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    category = Category.objects.get(slug=category_slug)
    products_of_category = Product.objects.filter(category=category)
    categories = Category.objects.all()
    context = {
        'category': category,
        'products_of_category': products_of_category,
        'categories': categories,
        'cart': cart
    }
    return render(request, 'category.html', context)


def cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    categories = Category.objects.all()
    context = {
        'cart': cart,
        'categories': categories
    }
    return render(request, 'cart.html', context)


def add_to_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.add_to_cart(product.slug)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    product.quantity -= 1
    product.save()
    return JsonResponse({
        'cart_total': cart.items.count(),
        'cart_total_price': cart.cart_total
    })


def remove_from_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.remove_from_cart(product.slug)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    product.quantity += 1
    product.save()
    return JsonResponse({
        'cart_total':cart.items.count(),
        'cart_total_price': cart.cart_total
    })


def change_item_qty(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    qty = request.GET.get('qty')
    item_id = request.GET.get('item_id')
    cart_item = CartItem.objects.get(id=int(item_id))
    cart_item.qty = int(qty)
    cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
    cart_item.save()
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({
        'cart_total': cart.items.count(),
        'item_total': cart_item.item_total,
        'cart_total_price': cart.cart_total
    })


def checkout_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    categories = Category.objects.all()
    context = {
        'cart': cart,
        'categories': categories,
    }
    return render(request, 'checkout.html', context)


def order_create_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    categories = Category.objects.all()
    form = OrderForm(request.POST or None)
    context = {
        'form': form,
        'cart': cart,
        'categories': categories,
    }
    return render(request, 'order.html', context)


def make_order_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    form = OrderForm(request.POST or None)
    categories = Category.objects.all()
    if form.is_valid():
        name = form.cleaned_data['name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        buying_type = form.cleaned_data['buying_type']
        address = form.cleaned_data['address']
        comments = form.cleaned_data['comments']

        new_order = Order.objects.create(
            user=request.user,
            items=cart,
            total=cart.cart_total,
            first_name=name,
            last_name=last_name,
            phone=phone,
            buying_type=buying_type,
            address=address,
            comments=comments
        )

        del request.session['cart_id']
        del request.session['total']
        return render(request, 'thank_you.html')
    return render(request, 'order.html', {'categories': categories})


def account_view(request):

    categories = Category.objects.all()
    order = Order.objects.filter(user=request.user).order_by('-id')
    orders = Order.objects.order_by('-id')
    total_price = 0
    for e in orders:
        total_price += e.total
    context = {
        'order': order,
        'categories': categories,
        'orders': orders,
        'total_price': total_price,
    }
    return render(request, 'account.html', context)


def registration_view(request):

    categories = Category.objects.all()
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']

        new_user.username = username
        new_user.set_password(password)
        new_user.email = email
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()

        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('base'))
    context = {
        'categories': categories,
        'form': form,
    }
    return render(request, 'registration.html', context)


def login_view(request):

    categories = Category.objects.all()
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('base'))
    context = {
        'categories': categories,
        'form': form,
    }
    return render(request, 'login.html', context)


def support_view(request):

    categories = Category.objects.all()
    form = CommentForm(request.POST or None)

    context = {
        'categories': categories,
        'form': form
    }
    return render(request, 'support.html', context)


def send_support_view(request):

    categories = Category.objects.all()
    form = CommentForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['name']
        comment = form.cleaned_data['comment']

        new_comment = Comment()
        new_comment.name = name
        new_comment.comment = comment
        new_comment.save()
    context = {
        'categories': categories,
    }
    return render(request, 'support_sended.html', context)
