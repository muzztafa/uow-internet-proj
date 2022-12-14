import datetime

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.urls import reverse

from .forms import OrderForm, InterestForm, LoginForm, RegisterForm, ForgetPasswordForm
from .models import Category, Product, Client, Order
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
import random
import string
from django.contrib.auth.models import User


# Create your views here.


def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]

    last_login = request.session.get("last_login")
    return render(request, 'myapp/index.html', {'cat_list': cat_list, 'last_login': last_login})

    if request.COOKIES.get("about_visits") != None:
        print("not none")
        curr = request.COOKIES.get("about_visits")
        response.set_cookie("about_visits", int(curr) + 1, expires=expiry_time)
    else:
        print("none")
        response.set_cookie("about_visits", "1", expires=expiry_time)
    return response


def detail(request, cat_no):
    prod_list = Product.objects.filter(category=cat_no)
    category = get_object_or_404(Category, id=cat_no)
    return render(request, 'myapp/detail.html', {'productList': prod_list, 'category': category})

def about(request):
    response = render(request, 'myapp/about.html', {"visits": request.COOKIES.get("about_visits")})
    expiry_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)

    if request.COOKIES.get("about_visits") != None:
        print("not none")
        curr = request.COOKIES.get("about_visits")
        response.set_cookie("about_visits", int(curr) + 1, expires=expiry_time)
    else:
        print("none")
        response.set_cookie("about_visits", "1", expires=expiry_time)
    return response

def detail(request, cat_no):
    prod_list = Product.objects.filter(category=cat_no)
    category = get_object_or_404(Category, id=cat_no)
    return render(request, 'myapp/detail.html', {'productList': prod_list, 'category': category})


def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/products.html', {'prodlist': prodlist})


@login_required(login_url='/myapp/login/')
def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    isClient = False
    if (request.user.is_staff == False):
        isClient = True
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
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'prodlist': prodlist, 'isClient': isClient})


@login_required(login_url='/myapp/login/')
def product_detail(request, prod_id):
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
    return render(request, 'myapp/product_detail.html', {'form': form, 'product': product})


# Task5 added myorders redirection when logged in
def user_login(request):
    if request.method == 'POST':
        form = LoginForm()
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                logged_in_date = datetime.date.today()
                request.session['last_login'] = str(logged_in_date)

                return HttpResponseRedirect(reverse('myapp:myorders'))
            else:
                messages.error(request, "Your account has been disabled.")
                return render(request, 'myapp/login.html', {'form': form})
        else:
            messages.error(request, "Invalid login details.")
            return render(request, 'myapp/login.html', {'form': form})

            # return render(request, 'myapp/login.html', {'form': form, 'msg': 'invalid'})
            # return HttpResponse('Invalid login details.')
    else:
        form = LoginForm()
        return render(request, 'myapp/login.html', {'form': form})


def forget_password(request):
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            try:
                userObj = User.objects.get(email=email)

                if (userObj):  # only send email if client exists
                    try:
                        # create a new pw
                        letters = string.ascii_lowercase
                        new_password = ''.join(random.choice(letters) for i in range(8))

                        print(new_password)
                        send_mail(
                            'Django App Password Reset',
                            'Your new password is: ' + new_password,
                            'internetapplications9@gmail.com',
                            [email],
                            fail_silently=False,
                        )
                        userObj.set_password(new_password)
                        userObj.save()
                        msg = "A new password has been emailed to you."
                    except:
                        messages.error(request, "There was an error sending email.")
                        return render(request, 'myapp/forget_password_form.html', {'form': form})
            except:
                messages.error(request, "No client exists with the following email address: " + email)
                return render(request, 'myapp/forget_password_form.html', {'form': form})
                msg = "No client exists with the following email address: " + email
            messages.success(request, msg)
            return HttpResponseRedirect(reverse(('myapp:login')))
    else:
        form = ForgetPasswordForm()
    return render(request, 'myapp/forget_password_form.html', {'form': form})


# Task5 added for redirecting to login page
@login_required(login_url='/myapp/login/')
def myorders(request):
    loggedInUser = request.user.get_username()
    orders = []
    if (request.user.is_staff == False):
        isClient = True
        clientObj = Client.objects.filter(username=loggedInUser)
        orders = Order.objects.filter(client=clientObj.get())

    else:
        isClient = False
    return render(request, 'myapp/myorders.html', {"isClient": isClient, "orderList": orders})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:login')))


# Task4 registration form
def user_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        # checking if form is valid or not
        if form.is_valid():
            # saving the user from form to database
            form.save()
            # returning sucess message
            messages.success(request, "Successfully registered")

            # redirecting to login page
            return HttpResponseRedirect(reverse('myapp:login'))

        # returning error message
        messages.error(request, "Invalid information, Registration failed.")
    else:
        # saving registerform data to form so that it can be available for html page
        form = RegisterForm()
    return render(request=request, template_name="myapp/register.html", context={"register_form": form})


def json_data(request):
    data = list(Category.objects.values())
    return JsonResponse(data, safe=False)
