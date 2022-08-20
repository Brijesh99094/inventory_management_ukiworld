from django.urls import path,include
from . import views
from django.contrib.auth.views import LoginView,LogoutView


urlpatterns = [
    path('',views.index,name='index'),
    path('Due/',views.due,name="due"),
    path('Due_paid/<id>',views.due_paid,name="due_paid"),
    path('DelPurchase/<id>',views.del_purchase,name='del_purchase'),
    path('DelSales/<id>',views.del_sales,name='del_sales'),
    path('Account/',views.account,name='account'),
    path('purchaseproduct/<id>',views.purchase_product,name='purchase_product'),
    path('users/',views.users,name='users'),
    path('purchase/',views.purchase,name='purchase'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(template_name='registration/home.html'), name='logout'),
    path('stock/',views.stock,name='stock'),
    path('supplier/',views.supplier,name='supplier'),
    path('Del_supplier/<id>',views.Del_supplier,name='del_supplier'),
    path('sales/',views.sales,name='sales'),
    path('salesdetail/<id>',views.sales_detail,name='sales_detail'),
    path('pdf_view/<id>', views.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_view/', views.ViewPDF1.as_view(), name="pdf_view1"),
    path('freeReg/',views.freeReg,name="freeReg"),
    path('delete_prod/<id>',views.delete_prod,name='delete_prod'),
    path('GetImei/',views.GetImei,name='GetImei'),
    path('Images/',views.images,name='images'),
]
