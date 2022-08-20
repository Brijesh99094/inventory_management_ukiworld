from django import forms
from .models import *

suppliers = Supplier.objects.all()
products = PurchaseHasProduct.objects.filter(pur_prod=False)
sales = Sales.objects.all()

class PurchaseForm(forms.ModelForm):
    supp = forms.ModelChoiceField(queryset=suppliers,widget=forms.Select(attrs={'class':'custom-select'}))
    class Meta():
        model = Purchase
        fields = ('date','supp','payment_type')

class PurchaseHasProductForm(forms.ModelForm):
    class Meta():
        model = PurchaseHasProduct
        fields = ('purchase','product','imei_no','price')

class SalesHasProductForm(forms.ModelForm):
    sales =   forms.ModelChoiceField(queryset=sales,widget=forms.Select(attrs={'class':'custom-select'}))
    product = forms.ModelChoiceField(queryset=products,widget=forms.Select(attrs={'class':'custom-select'}))
    class Meta():
        model = SalesHasProduct
        fields = ('sales','product','imei_no','price')
  
        

class ProdHasImgForm(forms.ModelForm):
    class Meta():
        model = ProductHasImg
        fields = '__all__'
