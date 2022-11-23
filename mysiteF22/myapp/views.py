import datetime

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.urls import reverse

from .forms import OrderForm, InterestForm, LoginForm
from .models import Category, Product, Client, Order
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.


def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]

    last_login=request.session.get("last_login")
    return render(request, 'myapp/index.html', {'cat_list': cat_list, 'last_login':last_login})


def about(request):
    response=render(request, 'myapp/about.html',{"visits":request.COOKIES.get("about_visits")})
    expiry_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)

    if request.COOKIES.get("about_visits") != None:
        print("not none")
        curr = request.COOKIES.get("about_visits")
        response.set_cookie("about_visits", int(curr)+1, expires=expiry_time)
    else:
        print("none")
        response.set_cookie("about_visits", "1", expires=expiry_time)
    return response


def detail(request, cat_no):
    prod_list = Product.objects.filter(category=cat_no)
    category = get_object_or_404(Category,id=cat_no)
    # response = HttpResponse()
    # print('detail')
    # print(category)
    # response.write('<p> Detail Page </p>')
    # response.write('<p> Warehouse Location: '+category.warehouse+ ' </p>')
    # for product in prod_list:
    #     para = '<p>' + str(product.name) + ': ' + str(product.price) + '</p>'
    #     response.write(para)
    # return response
    # return render(request, 'myapp/detail0.html', {'productList': prod_list, 'category': category})
    return render(request, 'myapp/detail.html', {'productList': prod_list, 'category': category})


def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/products.html', {'prodlist': prodlist})


def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                order.save()
                msg = 'Your order has been placed successfully.'
                product = Product.objects.get(id=order.product.id)
                product.stock = product.stock - order.num_units
                product.save()
            else:
                msg = 'We do not have sufficient stock to fill your order.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'prodlist': prodlist})

def product_detail (request, prod_id):
    product = get_object_or_404(Product, id=prod_id)
    print("prod det")
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            form_prod = form.cleaned_data
            if form_prod["interested"] == "1":
                product.interested = product.interested + 1
                product.save()
                return HttpResponseRedirect('/myapp/')
    else:
        form = InterestForm()
    return render(request, 'myapp/product_detail.html', {'form':form,'product': product})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                logged_in_date = datetime.datetime.utcnow()
                request.session['last_login'] = str(logged_in_date)

                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        form = LoginForm()
        return render(request, 'myapp/login.html',{'form':form})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:login')))

@login_required
def myorders(request):
    loggedInUser = request.user.get_username()
    orders = []
    if(request.user.is_staff==False):
        isClient = True
        clientObj = Client.objects.filter(username=loggedInUser)
        orders = Order.objects.filter(client=clientObj.get())

    else:
        isClient = False

    return render(request, 'myapp/myorders.html', {"isClient": isClient, "orderList":orders})
