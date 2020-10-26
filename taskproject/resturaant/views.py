from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Sum
from django.core import mail
import datetime
from .models import *
from .forms import *
from decimal import *
# Create your views here.
def homepage(request, food_category = None): 
    if(request.user.is_authenticated):
        customer = request.user.users.get()
        if(customer.type_of_user == "staff"):
            return HttpResponseRedirect("/create_coupons/")
        food_categories = Food_Category.objects.all()
        food_items = None
        if (food_category):
            try:
                category = Food_Category.objects.get(category__iexact=food_category)
                food_items = category.food_item.all()
            except:
                return HttpResponse("Following Category Doesn't exist")
        type_of_customer = Customer.objects.get(user=customer).type_of_customer
        return render(request, "homepage.html", {'is_authenticated' : True,
                                                 'type_of_customer': type_of_customer, 
                                                 'food_categories' : food_categories,                                                 'food_category' : food_category,
                                                 'food_items' : food_items})
    else:
        return render(request, "homepage.html", { 'is_authenticated' : False})        


def register(request):
    if(request.user.is_authenticated):
        return HttpResponse("Please <a href='/logout/'>logout</a> to continue")
    
    if (request.method == "GET"):
        register_form = UserRegistration()
        type_of_user = TypeOfUser()
        return render(request,'register_user.html',{
            'register_form' : register_form, 
            'type_of_user' : type_of_user
        })
    else:
        register_form = UserRegistration(request.POST)
        type_of_user  = TypeOfUser(request.POST)
        if (register_form.is_valid()):
            user =  register_form.save(commit = False)
            user.set_password(user.password) 
            USER_OF_WEBSITE = type_of_user.save(commit=False)
            print(USER_OF_WEBSITE.type_of_user)
            if(USER_OF_WEBSITE.type_of_user == 'staff'):
                user.is_staff = True
                user.is_active = False
            user.save()
            USER_OF_WEBSITE.user = user
            USER_OF_WEBSITE.save()
            if (USER_OF_WEBSITE.type_of_user == 'customer'):
                customer = Customer(user = USER_OF_WEBSITE, type_of_customer = 'normal')
                customer.save()
                return HttpResponse("Customer Created Successfully")
            else:
                return HttpResponse("Staff Member created successfully. Wait for your account to be activated.")
        else:
            return HttpResponse("Please provide correct details")

def user_login(request):
    if (request.user.is_authenticated):
        return HttpResponse("Please <a href='/logout/'>logout</a> to continue")
    if(request.method == "GET"):
        form = LoginForm()
        return render(request, 'login.html', {
            'form' : form
        })
    else:
        login_form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if (user):
            if (user.is_staff):
                if (user.is_active):
                    login(request, user)
                    return HttpResponseRedirect("/create_coupons/")
                else:
                    return HttpResponse("Your account hasn't been activated yet.")
            else:
                login(request, user)
                return HttpResponseRedirect("/")
        else:
            return HttpResponse("Incorrect Credentials")
        
def user_logout(request):
    if(not(request.user.is_authenticated)):
        return HttpResponse("Please <a href='/login/'>login</a> to continue")
    logout(request)
    return HttpResponseRedirect("/")
        
@login_required
def item_view(request, food_item):
    user = request.user.users.get()
    if(user.type_of_user == "staff"):
        return HttpResponseRedirect("/create_coupons/")
    if (request.method == "GET"):
        try:
            food_item = Food_Items.objects.get(item_name = food_item)
            return render(request, "item_view.html", {'food_item':food_item})
        except:
            return HttpResponse("Following item isnt served by us")
    else:
        food_item = Food_Items.objects.get(item_name = food_item)
        user = Customer.objects.get(user = user)
        quantity = request.POST['quantity']
        price = food_item.price
   
        try:
            cart = Cart.objects.get(user = user ,food_item = food_item, status = 'in_cart')
            cart.quantity = int(cart.quantity) + int(quantity)
            cart.price = cart.price + (price * Decimal(quantity))
            cart.save()
        except:
            price = price * Decimal(quantity)
            cart = Cart(user=user, food_item = food_item, quantity = quantity, price = price)
            cart.save()
        return HttpResponseRedirect('/')

@login_required
def cart_view(request, coupon = None):
    user = request.user.users.get()
    if (user.type_of_user == "staff"):
        return HttpResponseRedirect("/create_coupons/")
    customer = Customer.objects.get(user = user)
    cart = Cart.objects.filter(user = customer, status = 'in_cart')
    length_of_cart = Cart.objects.filter(user = customer, status = 'in_cart').count()
    price = 0
    for item in cart:
        price += item.price
    address = Address.objects.filter(user = customer)
    length = Address.objects.filter(user = customer).count()
    errors = None
    discount = None
    total_discount = 0
    
    if (request.method == 'GET'):
        return render(request, 'cart_view.html', {'customer' : customer,
                                                  'cart': cart,
                                                  'price':price,
                                                  'length' : length,
                                                  'address' : address,
                                                  'length_of_cart' : length_of_cart,
                                                  'errors' : errors,
                                                  'discount': discount,
                                                  'total_discount' : total_discount
                                                  })
                    
    elif (request.method == "POST" and not(coupon == None)):
        try:
            coupon = Coupons.objects.get(coupon_code__exact = request.POST['coupon_code'], expiry_date__gte = datetime.datetime.now().date())
            if(coupon.type_of_user == "both" or coupon.type_of_user == customer.type_of_customer):
                    try:
                        discount = Discount.objects.get(user = customer, status = "not_completed")
                        discount.coupon = coupon
                        discount.total_cost = discount.price - discount.price * Decimal(coupon.percent_discount / 100)
                        discount.save() 
                    except:
                        total_cost = price - price * Decimal(coupon.percent_discount / 100)
                        if(total_cost == 0):
                            return HttpResponseRedirect("/")
                        discount = Discount(user = customer, price = price, coupon = coupon, total_cost = total_cost)
                        discount.save()
                    total_discount = discount.price - discount.total_cost                
            else:
                errors = "You aren't eligible for this coupon."
        except:
            errors = "No such coupon exist"

        return render(request, 'cart_view.html', {'customer' : customer,
                                                  'cart': cart,
                                                  'price':price,
                                                  'length' : length,
                                                  'address' : address,
                                                  'length_of_cart' : length_of_cart,
                                                  'errors' : errors,
                                                  'discount': discount,
                                                  'total_discount' : total_discount
                                                  })

    else:
        address_pk = request.POST['address']
        address = Address.objects.get(id = address_pk)
        try:
            discount = Discount.objects.get(user = customer, status = "not_completed")
            total_cost = Decimal(discount.total_cost)
            order = Order(user = customer, address = address, total_cost = total_cost)
        except:
            order = Order(user = customer, address = address, total_cost = price)
        order.save()
        for item in cart:
            cart = Cart.objects.get(id = item.id)
            cart.status = 'done'
            cart.save()
            order.item_ordered.add(item.food_item)
        try:
            discount = Discount.objects.get(user = customer)
            discount.delete()
        except:
            pass
        total_order = Order.objects.filter(order_status = 'ndel', time_of_order__date=datetime.datetime.now().date()).exclude(user = customer).count()
        user_order = Order.objects.filter(user = customer, order_status = 'ndel', time_of_order__date=datetime.datetime.now().date()).count()
        total_time = (total_order * 15) + (10 * user_order) + 5
        return render(request, 'order_placed.html', {'total_time' : total_time,
                                                     'order' : order})
@login_required
def empty_cart(request):
    user = request.user.users.get()
    if (user.type_of_user == "staff"):
        return HttpResponseRedirect("/create_coupons/")
    customer = Customer.objects.get(user = user)
    cart = Cart.objects.filter(user = customer, status = 'in_cart')
    for item in cart:
        item.delete()
    return HttpResponseRedirect('/')

@login_required
def addresses (request):
    user = request.user.users.get()
    if (user.type_of_user == "staff"):
        return HttpResponseRedirect("/create_coupons/")
    customer = Customer.objects.get(user = user)
    if (request.method == 'GET'):
        addresses = Address.objects.filter(user = customer)
        address_form = AddressForm()
        return render (request, 'address.html', {'addresses' : addresses,
                                                 'address_form' : address_form})                                        
    else:
        address_form = AddressForm(request.POST)
        if (address_form.is_valid()):
            address = address_form.save(commit = False)
            address.user = customer
            address.save()
            return HttpResponseRedirect('/addresses/')
        else:
            return HttpResponseRedirect('/addresses/')

@login_required
def previous_order (request):
    user = request.user.users.get()
    if (user.type_of_user == "staff"):
        return HttpResponseRedirect("/create_coupons/")
    customer = Customer.objects.get(user = user)
    order = Order.objects.filter(user = customer).order_by('-time_of_order')
    total_order  = Order.objects.filter(user = customer).count()
    return render(request, 'previous_order.html', {'order' : order,
                                                   'customer' : customer,
                                                   'total_order': total_order})

@login_required
def feedback (request, id):
    user = request.user.users.get()
    if (user.type_of_user == "staff"):
        return HttpResponseRedirect("/create_coupons/")

    order_feedback = Order.objects.get(id = id)
    try:
        feedback = Feedback.objects.get(order = order_feedback)
        return HttpResponse("You've already provided your valuable feedbacks for this order")
    except:    
        customer = Customer.objects.get(user = user)
        order = Order.objects.filter(user = customer)

        if (request.method == "GET"):
            if (order_feedback in order):
                form = FeedbackForm()
                return render(request, 'feedback.html', {'order_feedback': order_feedback,
                                                        'form' : form})
            else:
                return HttpResponse("You can't provide feedback for this order")
        else:
            form = FeedbackForm(request.POST)
            if form.is_valid():
                feedback =  form.save(commit = False)
                feedback.user = customer
                feedback.order = order_feedback
                feedback.save()
                return HttpResponseRedirect("/")
            else:
                return HttpResponseRedirect("/")

@login_required
def create_coupon (request):
    user = request.user.users.get()
    if (user.type_of_user == "customer"):
        return HttpResponse("This view is restricted only for staff members.")
    if (request.method == "GET"):
        coupon_form = CouponForm()
        return render (request, "create_coupon.html", {"coupon_form" : coupon_form})
    else:
        coupon_form = CouponForm(request.POST)
        if coupon_form.is_valid():
            coupon = coupon_form.save(commit = False)
            coupon.percent_discount = Decimal(coupon.percent_discount)
            coupon.save()
            if (coupon.type_of_user == "both"):
                customer = Customer.objects.all()
            else:
                customer = Customer.objects.filter(type_of_customer = coupon.type_of_user)
            send_to = []
            for info in customer:
                print(info.user.user.email)
                send_to += [info.user.user.email]
            coupon_code = coupon.coupon_code
            expiry_date = coupon.expiry_date
            percent_discount = coupon.percent_discount
            subject = "New Coupon from Resturant"
            message = "Hey there is a new coupon we've created just for you.Coupon Code is '" +coupon_code + "'.Use it before " + str(expiry_date) + " to get " + str(percent_discount) + "% off on your next order."
            mail.send_mail(subject, message, "sarthak.rsp@gmail.com",send_to,fail_silently=False)
            return HttpResponse("Mail regarding coupons has been sent successfully to respective users.")
        else:
            return HttpResponseRedirect('/create_coupons/')

@login_required
def go_premium(request):
    user = request.user.users.get()
    if (user.type_of_user == "staff"):
        return HttpResponseRedirect("/create_coupons/")
    customer = Customer.objects.get(user = user)
    type_of_customer = customer.type_of_customer
    if (type_of_customer == 'premium'):
        return HttpResponse("You are already a premium member")
    if(request.method == "GET"):
        return render(request, "go_premium.html")
    else:
        customer = Customer.objects.get(user = user)
        customer.type_of_customer = "premium"
        customer.save()
        return HttpResponse("You're a premium member now.")

@login_required
def view_coupons(request):
    user = request.user.users.get()
    if (user.type_of_user == "staff"):
        return HttpResponseRedirect("/create_coupons/")
    customer = Customer.objects.get(user = user)
    type_of_customer = customer.type_of_customer
    if(type_of_customer == 'premium'):
        coupons = Coupons.objects.exclude(type_of_user = 'normal').exclude(expiry_date__lt=datetime.datetime.now().date())
    else:
        coupons = Coupons.objects.exclude(expiry_date__lt=datetime.datetime.now().date())
    return render(request, "view_coupon.html", {'coupons' : coupons,
                                                'type_of_customer' : type_of_customer})


    
@login_required
def view_meal(request):
    user = request.user.users.get()
    if (user.type_of_user == "staff"):
        return HttpResponseRedirect("/create_coupons/")
    customer = Customer.objects.get(user = user)
    type_of_customer = customer.type_of_customer
    if(type_of_customer == 'premium'):
        meals = Meals.objects.exclude(type_of_user = "normal")
    else:
        meals = Meals.objects.all()
    return render(request, "view_meals.html", {'meals' : meals,
                                               'type_of_customer' : type_of_customer})

@login_required
def add_meal(request, id):
    user = request.user.users.get()
    if (user.type_of_user == "staff"):
        return HttpResponseRedirect("/create_coupons/")
    customer = Customer.objects.get(user = user)
    type_of_customer = customer.type_of_customer
    try:
        meal = Meals.objects.get(id = id)
        if(meal.type_of_user == "both" or meal.type_of_user == type_of_customer):
            for item in meal.meal.all():
                try:
                    cart = Cart.objects.get(user = customer, food_item = item.food_item, status = "in_cart")
                    cart.quantity += item.quantity
                    cart.price +=  item.price
                    cart.save()
                except:
                    price = item.price
                    cart = Cart(user = customer, food_item = item.food_item, quantity = item.quantity, price = price)
                    cart.save()
            return HttpResponseRedirect("/")
        else:
            return HttpResponse("Following meal is not available for you.")
    except:
        return HttpResponse("Following meal is not served by us.")

@login_required
def create_meal(request):
    user = request.user.users.get()
    if (user.type_of_user == "customer"):
        return HttpResponse("This view is restricted only for staff members.")
    if (request.method == "GET"):
        meal_form = MealForm()
        meals = Meals.objects.all()
        return render(request, "view_meal_staff.html", {'meals' : meals,
                                                        'meal_form' : meal_form})
    else:
        meal_form = MealForm(request.POST)
        if meal_form.is_valid():
            meal = meal_form.save()            
            return HttpResponseRedirect('/meal/' + str(meal.id))
        else:
            return HttpResponse("Meal hasn't been created")

@login_required
def add_meal_item(request, id):
    user = request.user.users.get()
    if (user.type_of_user == "customer"):
        return HttpResponse("This view is restricted only for staff members.")
    if (request.method == "GET"):
        try:
            meal = Meals.objects.get(id = id)
            length = MealItem.objects.filter(meals = meal).count()
            meal_item_form = MealItemForm()
            return render(request, "add_meal_item.html", {"meal" : meal,
                                                          "length" : length,
                                                          "meal_item_form":meal_item_form})
        except:
            return HttpResponse("No such meal exist.")
    else:
        meal_item_form = MealItemForm(request.POST)
        if(meal_item_form.is_valid()):
            meal = Meals.objects.get(id =id)
            meal_item = meal_item_form.save(commit =False)
            try:
                meal_already_present_item = MealItem.objects.get(meals = meal, food_item = meal_item.food_item)
                meal_already_present_item.quantity += meal_item.quantity
                meal_already_present_item.price += ((meal_item.food_item.price - meal_item.food_item.price * Decimal(0.10)) * Decimal(meal_item.quantity))
                meal.price += ((meal_item.food_item.price - meal_item.food_item.price * Decimal(0.10)) * Decimal(meal_item.quantity))
                meal_already_present_item.save()
                meal.save()
            except:
                meal_item.meals = meal
                meal_item.price = ((meal_item.food_item.price - meal_item.food_item.price * Decimal(0.10)) * Decimal(meal_item.quantity))
                meal.price += meal_item.price 
                meal_item.save()
                meal.save()
            return HttpResponseRedirect("/meal/" + str(id))
        else:
            return HttpResponse("Item hasn't been added")

@login_required
def remove_meal_item (request, id):
    user = request.user.users.get()
    if (user.type_of_user == "customer"):
        return HttpResponse("This view is restricted only for staff members.")
    try:
        meal_item = MealItem.objects.get(id = id)
        id = meal_item.meals.id
        meal_item.delete()
        return HttpResponseRedirect("/meal/" + str(id))
    except:
        return HttpResponse("Meal item not removed")

@login_required
def filter_price(request):
    user = request.user.users.get()
    if (user.type_of_user == "staff"):
        return HttpResponseRedirect("/create_coupons/")
    if(request.POST):
        max_price = request.POST['max_price']
        food_items = Food_Items.objects.filter(price__lte = max_price)
        length = Food_Items.objects.filter(price__lte = max_price).count()
        return render(request, "filter_by_price.html", {'food_items' : food_items,
                                                        'length' : length})
    else:
        return HttpResponseRedirect("/")

@login_required
def search_bar(request):
    user = request.user.users.get()
    if (user.type_of_user == "staff"):
        return HttpResponseRedirect("/create_coupons/")
    if(request.POST):
        search = request.POST['search']
        food_items = Food_Items.objects.filter(item_name__icontains = search)
        length = Food_Items.objects.filter(item_name__icontains = search).count()
        return render(request, "search_item.html", {"food_items" : food_items,
                                                    "length" : length})
    else:
        return HttpResponseRedirect("/")
        
