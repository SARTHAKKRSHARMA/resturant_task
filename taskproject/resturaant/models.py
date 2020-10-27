from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class DaysOfTheWeek(models.Model):
    CHOICES = (
        ( "0", "Monday"),
        ( "1", "Tuesday"),
        ( "2", "Wednesday"),
        ( "3", "Thursday"),
        ( "4", "Friday"),
        ( "5", "Saturday"),
        ( "6", "Sunday")
    )
    day_of_the_week = models.CharField(max_length = 15, choices = CHOICES)
    def __str__(self):
        return self.day_of_the_week

class Food_Category (models.Model):
    TYPE_OF_FOOD = (
        ("veg", "Vegetarian"),
        ("non-veg", "Non-Vegetarian")
    )
    type_of_category = models.CharField(max_length = 30,choices = TYPE_OF_FOOD, default="veg")
    category = models.CharField(max_length = 50)
    def __str__(self):
        return self.category

class Food_Items (models.Model):
    item_type = models.ForeignKey(Food_Category, on_delete=models.CASCADE, related_name='food_item')
    item_name = models.CharField(max_length = 50)
    description = models.TextField(blank = True)
    image = models.ImageField(blank = True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    days_of_avaibility = models.ManyToManyField(to = DaysOfTheWeek)
    start_time = models.TimeField(default = "08:00:00")
    end_time = models.TimeField(default = "22:00:00")
    quantity_available = models.IntegerField(default =50)
    def __str__(self):
        return self.item_name


class user_of_website(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    TYPE_OF_USER = (
        ('customer', 'Customer'),
        ('staff', 'Staff')
    )
    type_of_user = models.CharField(max_length = 8, choices = TYPE_OF_USER) 

    def __str__(self):
        return self.user.username


class Customer(models.Model):
    TYPE_OF_CUSTOMER = (
        ('premium', 'Premium'),
        ('normal', 'Normal')
    )
    user = models.OneToOneField(user_of_website, on_delete=models.CASCADE)
    type_of_customer = models.CharField(max_length = 15, choices = TYPE_OF_CUSTOMER)

    def __str__(self):
        return self.user.user.username


class Cart (models.Model):
    STATUS = (
        ('in_cart', "In Cart"),
        ('done', "Done")
    )
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer_cart", blank=True, null=True)
    food_item = models.ForeignKey(Food_Items, on_delete=models.CASCADE, related_name="cart_items", blank=True, null=True)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=15, decimal_places=2, default = 0)
    status = models.CharField(max_length = 25, choices = STATUS, default = "in_cart")


class Address(models.Model):
    TYPE_OF_ADDRESS = (
        ('home', "Home"),
        ('work', 'Work'),
        ('other', 'Other')
    )
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer_address")
    type_of_address = models.CharField(max_length = 15, choices = TYPE_OF_ADDRESS, default = "home")
    address_line_1 = models.CharField(max_length = 500, blank = False)
    address_line_2 = models.CharField(max_length = 300, blank = True)
    city = models.CharField(max_length = 50)
    state = models.CharField(max_length = 50)
    postal_code = models.PositiveIntegerField()

    def __str__(self):
        return self.type_of_address + "@" + self.user.user.user.username


class Order (models.Model):
    ORDER_STATUS = (
        ("del", "Delivered"),
        ('ndel', "Not Delivered")
    )
    user = models.ForeignKey(Customer, on_delete = models.CASCADE, related_name="customer_order")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="delivery_address")
    item_ordered = models.ManyToManyField(Food_Items)
    total_cost = models.DecimalField(max_digits=15, decimal_places=2)
    time_of_order = models.DateTimeField(default = timezone.now)
    order_status = models.CharField(max_length = 50, choices = ORDER_STATUS, default='ndel')

    def __str__(self):
        return self.user.user.user.username


# class ItemOrdered (models.Model):
#     order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name = "item_ordered")
#     food_item = models.ForeignKey(Food_Items, on_delete=  models.CASCADE, related_name = "item_name")
#     quantity = models.IntegerField()
#     price = models.DecimalField(max_digits=14, decimal_places=2)


class Feedback (models.Model):
    FEEDBACK = (
        ('1', "Bad"),
        ('2', "Good"),
        ('3', "Excellent")
    )
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="user_feedback")
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    food_packaging = models.CharField(max_length = 15, choices = FEEDBACK)
    food_taste = models.CharField(max_length = 15, choices = FEEDBACK)
    delivery_services = models.CharField(max_length = 15, choices = FEEDBACK)
    other_feedback = models.TextField(blank = True, null =True)

    def __str__ (self):
        return self.user.user.user.username

class Coupons (models.Model):
    TYPE_OF_USER = (
        ('both', 'Both'),
        ('normal', 'Normal'),
        ('premium', 'Premium')
    )
    type_of_user = models.CharField(max_length = 15, choices = TYPE_OF_USER, default = 'premium')
    coupon_name = models.CharField(max_length = 20, blank = True, null =True)
    coupon_description = models.TextField(blank = True, null = True)
    coupon_code = models.CharField(max_length = 20)
    percent_discount = models.DecimalField(max_digits=4, decimal_places=2)
    expiry_date = models.DateField(blank = True, null =True)
    def __str__(self):
        return self.coupon_code


class Discount (models.Model):
    STATUS = (
        ('completed', "Completed"),
        ('not_completed', "Not Completed")
    )
    user = models.ForeignKey(Customer, on_delete = models.CASCADE, related_name="user_discount")
    coupon = models.ForeignKey(Coupons, on_delete = models.CASCADE, related_name="user_coupon")
    price = models.DecimalField(max_digits=15, decimal_places=2)
    total_cost = models.DecimalField(max_digits= 15, decimal_places=2)
    status = models.CharField(max_length=15, choices = STATUS, default = "not_completed")

class Meals (models.Model):
    TYPE_OF_USER = (
        ('both', "Both"),
        ('normal', "Normal"),
        ('premium', "Premium")
    )
    meal_name = models.CharField(max_length=15, blank = True, null = True)
    type_of_user = models.CharField(max_length=20, choices=TYPE_OF_USER, default = 'premium')
    meal_start_time = models.TimeField(default = "08:00:00")
    meal_end_time = models.TimeField(default = "22:00:00")
    price = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)

class MealItem (models.Model):
    meals = models.ForeignKey(Meals,on_delete= models.CASCADE, related_name="meal")
    food_item = models.ForeignKey(Food_Items, on_delete=models.CASCADE, related_name="meal_items", blank=True, null=True)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=15, decimal_places=2, default = 0)

    
