from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *

class UserRegistration(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password', 'username', 'email')

class TypeOfUser(ModelForm):
    class Meta:
        model = user_of_website
        fields = ('type_of_user',)

class LoginForm (ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'password')

class AddressForm (ModelForm):
    class Meta:
        model = Address
        fields = ('type_of_address','address_line_1','address_line_2','state','city','postal_code')

class FeedbackForm (ModelForm):
    class Meta:
        model = Feedback
        fields = ('food_packaging', 'food_taste', 'delivery_services', 'other_feedback')

class CouponForm (ModelForm):
    class Meta:
        model = Coupons
        fields = ('type_of_user', 'coupon_name', 'coupon_description', 'coupon_code', 'percent_discount', 'expiry_date')
    
class MealForm (ModelForm):
    class Meta:
        model = Meals
        fields = ('meal_name','type_of_user')

class MealItemForm (ModelForm):
    class Meta:
        model = MealItem
        fields = ('food_item', 'quantity')

