from django.contrib import admin
from . models import *

# Register your models here.

class purchase(admin.ModelAdmin):
    list_display = ('id','supp','date','payment_type')
    search_fields = ('id', 'payment_type')
admin.site.register(Purchase,purchase)

class purchasehasproduct(admin.ModelAdmin):
    list_display = ('id','product','imei_no','price','purchase','pur_prod')
    search_fields = ('id', 'product','imei_no')
admin.site.register(PurchaseHasProduct,purchasehasproduct)


class supplier(admin.ModelAdmin):
    list_display = ('id','supp_name','phone')
    search_fields = ('id', 'supp_name','phone')
admin.site.register(Supplier,supplier)

class sales(admin.ModelAdmin):
    list_display = ('id','customer','phone','date')
    search_fields = ('id','customer','phone','date')
admin.site.register(Sales,sales)

class salesdetail(admin.ModelAdmin):
    list_display = ('id','sales','product','imei_no','price')
    search_fields = ('id','product','imei_no')
admin.site.register(SalesHasProduct,salesdetail)

class account(admin.ModelAdmin):
    list_display = ('id','date','amount','remark','check')
    search_fields = ('id','date','amount')
admin.site.register(Account,account)


class Image(admin.ModelAdmin):
     list_display = ('id','prod')
     search_fields = ('id','prod')
admin.site.register(ProductHasImg,Image)


