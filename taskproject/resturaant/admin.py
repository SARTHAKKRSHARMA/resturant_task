import os
from django.conf import settings
from django.contrib import admin
from .models import *
from openpyxl import Workbook, load_workbook
from django.utils import timezone
import datetime
# Register your models here.

def generate_excel (ModelAdmin, request, queryset):
    date = datetime.datetime.now().date()
    filepath = os.path.join(settings.BASE_DIR, "sales.xlsx")
    data = load_workbook(filepath)
    sheet = data.active
    empty_row = ("","","","","","","")
    row_1 = ("", "Sale on ", str(timezone.now().date()),"", "")
    row_2 = ("username","type_of_user","ordered_at", "Item Ordered","Total Amount","Order_Status")
    sheet.append(empty_row)
    sheet.append(empty_row)
    sheet.append(row_1)
    sheet.append(row_2)
    for order in queryset:
        if (order.time_of_order.date() == timezone.now().date()):
            username = order.user.user.user.username
            type_of_user = order.user.type_of_customer
            ordered_at = str(order.time_of_order.time())
            total_amount = order.total_cost
            order_status = order.order_status
            item_ordered = []
            for item in order.item_ordered.all():
                item_ordered += [item.item_name]
            data_row = (username,type_of_user,ordered_at,str(item_ordered) ,total_amount,order_status)
            sheet.append(data_row)
            data.save(filepath)



class DataAdmin(admin.ModelAdmin):
    actions = [generate_excel,]


admin.site.register(user_of_website)
admin.site.register(Address)
admin.site.register(Customer)
admin.site.register(Food_Category)
admin.site.register(Food_Items)
admin.site.register(Order, DataAdmin)
admin.site.register(Feedback)
admin.site.register(Cart)
admin.site.register(Coupons)
admin.site.register(Discount)

class MealInline(admin.TabularInline):
    model = MealItem
    raw_id_fields = ['food_item']

@admin.register(Meals)
class MealAdmin(admin.ModelAdmin):
    inlines = [MealInline]