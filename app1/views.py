from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import *
from django.contrib import messages
from django.utils.timezone import datetime
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views import View
from django.db.models import Q
from django.contrib.auth import get_user_model

###############################################################
############################ PDF  #############################
###############################################################

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

# Opens up page as PDF
class ViewPDF(View):
    def get(self, request, id, *args, **kwargs):
        salesObj = Sales.objects.get(id=id)
        sales_prodObj = SalesHasProduct.objects.filter(sales=salesObj.id)
        total = 0
        for sp in sales_prodObj:
            total += (sp.price)

        context = {'sales_data': salesObj,
                   'shp': sales_prodObj, 'total': total}
        pdf = render_to_pdf('registration/pdf_template.html', context)
        return HttpResponse(pdf, content_type='application/pdf')

class ViewPDF1(View):

    def get(self, request, *args, **kwargs):
        try:
            p1  = Purchase.objects.filter(Q(payment_type='Cash')|Q(payment_type='Jamin acc')|Q(payment_type='Jamin machine')|Q(payment_type='Urvesh machine')|Q(payment_type='Chintan machine')|Q(payment_type='Urvesh hdfc saving :- 8918')|Q(payment_type='Urvesh yes current')|Q(payment_type='Urvesh hdfc current :- 6983'),date=datetime.now())
            pd =  PurchaseHasProduct.objects.all()
            
            s1  = Sales.objects.filter(date=datetime.now())
            sd =  SalesHasProduct.objects.all()
            
            
            
        except Exception as e:
            print(e)
        d1 = datetime.now()
        d2 =d1.strftime('%B %d, %Y')
        context = {'p1':p1,'pd':pd,'sale':s1,'shp':sd,'d1':d2}
        pdf = render_to_pdf('registration/pdf_template1.html', context)
        return HttpResponse(pdf, content_type='application/pdf')

###############################################################
############################ end of PDF  ######################
###############################################################

def getAmount(payment_type):
    if payment_type=="Due":
        return "Due"
    a1 = Account.objects.get(remark=payment_type)
    return a1.amount


def get_tt():
    a1 = Account.objects.all()
    amt=0
    for a in a1:
        if a.check == False:
            amt += a.amount
        else:
            amt -= a.amount
    return amt

def profit_loss():
    pObj = PurchaseHasProduct.objects.raw("select * from app1_purchasehasproduct where purchase_id in (select id from app1_purchase where payment_type = 'Cash' or payment_type = 'Jamin acc' or payment_type = 'Jamin machine' or payment_type = 'Urvesh machine' or payment_type = 'Chintan machine' or payment_type = 'Urvesh hdfc saving :- 8918' or payment_type = 'Urvesh hdfc current :- 6983' or payment_type = 'Urvesh yes current' )")
    sObj = SalesHasProduct.objects.all()
    str1=""
    p=0
    s=0
    for i in pObj:
        p +=i.price
    for j in sObj:
        s += j.price
    pf = s-p
    if pf < 0:
        str1 = "Loss"
    else:
        str1 = "Profit"
    return  abs(p-s),str1
    
def get_due():
    d = 0
    p1 = Purchase.objects.filter(payment_type='Due')
    pd = PurchaseHasProduct.objects.all()
    for i in p1:
        for j in pd:
            if i == j.purchase:
                d += j.price
    return d



@login_required(login_url='login')
def due(request):
    obj = Purchase.objects.filter(payment_type="Due")
    php = PurchaseHasProduct.objects.all()
    supp = Supplier.objects.all()
    context={'pur':obj,'php':php,'supp':supp}
    return render(request,"registration/due.html",context)


@login_required(login_url='login')
def index(request):
    coh = get_tt()
    pl,status = profit_loss()
    due = get_due()
    user = request.user
    acc = Account.objects.filter(is_acc=True)
    context={"amt":coh,"pl":pl,"status":status,'due':due,'user':user,'acc':acc}
    return render(request,"registration/index.html",context)
    

def delete_prod(request,id):
    if request.POST:
        php = PurchaseHasProduct.objects.get(id=id)
        if php.purchase.id == 1:
            php.delete()
            messages.success(request,"Product deleted")
            return redirect('stock')
        else:
            messages.warning(request,"You can not delete this product")
            return redirect('stock')


@login_required(login_url='login')
def users(request):
    form = UserCreationForm()
    User = get_user_model()
    users = User.objects.all()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            #login(request, user)
            return redirect('users')
    else:
        form = UserCreationForm()
    return render(request,"registration/reg.html",{'form': form,'users':users})


@login_required(login_url='login')
def del_purchase(request,id):
    if request.POST:
        check=False
        purObj = Purchase.objects.get(id=id)
        php = PurchaseHasProduct.objects.filter(purchase=purObj)
        for i in php:
            if i.pur_prod==False:
                continue
            else:
                check = True
                messages.warning(request,"You can not delete this purchase")
                return redirect('purchase')
    if check == False:
        for i in php:
            if purObj.payment_type == "Cash" or purObj.payment_type == "Jamin acc" or purObj.payment_type == "Jamin machine" or purObj.payment_type == "Urvesh machine" or  purObj.payment_type == "Chintan machine" or purObj.payment_type == "Urvesh hdfc saving :- 8918" or purObj.payment_type == "Urvesh yes current" or purObj.payment_type == "Urvesh hdfc current :- 6983":
                a2 = Account.objects.get(remark=purObj.payment_type,is_acc=True)
                a2.amount += i.price
                a2.save()
                a1 = Account.objects.create(date=datetime.now(),amount=i.price,remark=f"{i.product} deleted from purchase",check=False)
                a1.save()
                i.delete()
            else:
                i.delete()
        purObj.delete()
        messages.success(request,"Purchase deleted")
        return redirect('purchase')

        
        


@login_required(login_url='login')
def purchase(request,*args,**kwargs):
    form = PurchaseForm()
    pur = Purchase.objects.all()
    php = PurchaseHasProduct.objects.all()
    if request.POST:
        form = PurchaseForm(request.POST)
        if form.is_valid():
            type = form.cleaned_data["payment_type"]
            try:
                acc = Account.objects.get(remark=type) 
            except:
                messages.warning(request,"Create account first")
                return redirect("purchase")
            
            amnt = getAmount(type)
            if amnt=="Due":
                    p = form.save()
                    pid = p.id
                    return redirect('purchase_product',pid)
                 
            else:
                if amnt<=0 :
                    messages.warning(request,f"Insufficient balance,For more information check Account")
                    return redirect('purchase')
            p = form.save()
            pid = p.id
            return redirect('purchase_product',pid)
    context = {'form':form,'pur':pur,'php':php}
    return render(request,"registration/tab-Admin-purchase.html",context)


@login_required(login_url='login')
def purchase_product(request,id):
    form = PurchaseHasProductForm()
    pid = Purchase.objects.get(id=id)
    items = PurchaseHasProduct.objects.filter(purchase=pid)
    imgs = ProductHasImg.objects.all()
    img_form = ProdHasImgForm()
    context={'form':form,'pid':pid,'items':items,'img_form':img_form,'imgs':imgs}
    if request.POST:
        img_form = ProdHasImgForm(request.POST,request.FILES)
        if img_form.is_valid():
            img_form.save()
            messages.success(request,"image uploded")
            return redirect('purchase_product',id)
        form = PurchaseHasProductForm(request.POST)
        if form.is_valid():
            amt = form.cleaned_data['price']
            product = form.cleaned_data['product']
            acc_amt = getAmount(pid.payment_type)
            if acc_amt == "Due":
                form.save()
                messages.success(request,"Product Added")
                return redirect('purchase_product',id)
            if amt <= acc_amt:
                form.save()
            else:
                messages.warning(request,"This account has not sufficient amount")
                return redirect('purchase_product',id)
                return redirect('purchase_product',id)
            if pid.payment_type == "Cash" or pid.payment_type == "Jamin acc" or pid.payment_type == "Jamin machine" or pid.payment_type == "Urvesh machine" or pid.payment_type == "Chintan machine" or pid.payment_type == "Urvesh hdfc saving :- 8918" or pid.payment_type == "Urvesh hdfc current :- 6983" or pid.payment_type == "Urvesh yes current":
                acc =  Account.objects.get(remark=pid.payment_type)
                acc.amount -= amt
                acc.save()
                a1 = Account.objects.create(date=datetime.now(),amount=amt,remark=f"Purchase of  {product} from { pid.supp } ",check=True,is_acc=False)
                a1.save()
           
                
                
            messages.success(request,"Product Added")
            return redirect('purchase_product',id)
           
        else:
            return HttpResponse('Form hass error')
#Add something when you are posting the form in html and view both
    return render(request,"registration/add_item.html",context)



#  return HttpResponse('Form hass error')
#             img_form = ProdHasImgForm(request.POST,request.FILES)
#             if img_form.is_valid():
#                 img_form.save()
#                 messages.success(request,"Image uploded")
#                 return redirect('purchase_product',id)
#             else:
#                 return HttpResponse('Form hass error')


@login_required(login_url='login')
def supplier(request):
    items = Supplier.objects.all()
    context={'items':items}
    if request.POST:
        name = request.POST.get('supp_name')
        phone = request.POST.get('mob')
        supObj = Supplier.objects.create(supp_name=name,phone=phone)
        supObj.save()
        messages.success(request,"Supplier Added")
    return render(request,"registration/supplier.html",context)
    

def Del_supplier(request,id):
    if request.POST:
        supp1 = Supplier.objects.get(id=id)
        try:
            supp1.delete()
        except Exception as e:
            messages.warning(request,"You can not delete this supplier")
            return redirect('supplier')
        messages.warning(request,"supplier Deleted")
        return redirect('supplier')


@login_required(login_url='login')
def stock(request):
    imgs = ProductHasImg.objects.all()
    pur_detail = PurchaseHasProduct.objects.filter(pur_prod=False)
    pur1 = Purchase.objects.get(payment_type="none")
    context={'items':pur_detail,'pur1':pur1,'imgs':imgs}
    return render(request,"registration/stock.html",context)





@login_required(login_url='login')
def sales(request):
    pur = Sales.objects.all()
    php = SalesHasProduct.objects.all()
    context={'pur':pur,'php':php}
    if request.POST:
        customer = request.POST.get("customer_name")
        mob = request.POST.get("mob")
        date = request.POST.get("date")
        salObj = Sales.objects.create(customer=customer,phone=mob,date=date)
        salObj.save()
        print(salObj)
        sales_id = salObj.id
        
        return redirect('sales_detail',sales_id)
    return render(request,"registration/sales.html",context)

@login_required(login_url='login')
def sales_detail(request,id):
    sales_detail_form = SalesHasProductForm()
    sid = Sales.objects.get(id=id)
    php = PurchaseHasProduct.objects.filter(pur_prod=False)
    items = SalesHasProduct.objects.filter(sales=sid)
    context={'sales_detail_form':sales_detail_form,'sid':sid,'items':items,'php':php}
    if request.POST:
        sales_detail_form = SalesHasProductForm(request.POST)
        if sales_detail_form.is_valid():
            imei_no = sales_detail_form.cleaned_data['imei_no']
            try:
                prod1 = PurchaseHasProduct.objects.get(imei_no=imei_no)
            except Exception as e:
                messages.success(request,"Please enter correct imei_no")
                print(e)
                return redirect('sales_detail',id)
            sales_detail = sales_detail_form.save()
            amt = sales_detail_form.cleaned_data['price']
            prod1.pur_prod = True
            prod1.save()
            a1 = Account.objects.create(date=datetime.now(),amount=amt,remark=f"{prod1} sold to { sid.customer } ",check=False)
            a1.save()
            acc= Account.objects.get(remark="Cash")
            acc.amount+=amt
            acc.save()
            return redirect('sales_detail',id)

    return render(request,"registration/sales_detail.html",context)


@login_required(login_url='login')
def del_sales(request,id):
    if request.POST:
        SaleObj = Sales.objects.get(id=id)
        php = SalesHasProduct.objects.filter(sales=SaleObj)
        cnt = php.count()
        if cnt <1:
            SaleObj.delete()
            return redirect('sales')
        for i in php:
            pdp = PurchaseHasProduct.objects.get(pur_prod=True,imei_no=i.imei_no)
            if pdp:
                pdp.pur_prod = False
                pdp.save()
                a1 = Account.objects.create(date=datetime.now(),amount=i.price,remark=f"{i.product} deleted from sales",check=True)
                a1.save()
                i.delete()
            else:
                messages.warning(request,"SOmethong goes wrong")
        SaleObj.delete()
        print(i.product,i.imei_no,i.price)
        return redirect('sales')
    pass


@login_required(login_url='login')
def account(request):
    a1 = Account.objects.all()
    var1  = get_tt() 
    if request.POST:
        date = datetime.now()
        amt = request.POST.get('amount')
        remark = request.POST.get('remark')
        acc = request.POST.get('acc')
        cr_dr = request.POST.get('cr_dr')
        
        
        #Account creation
        if remark == "" and acc != "" and cr_dr == "credit":
            a1,created= Account.objects.get_or_create(remark=acc, defaults={"amount": amt, "check": False,"date":date,"is_acc":True})
            if created:
                messages.success(request,"Account created")
            else:
                a1.amount += int(amt)
                a1.save()
        
        
        #Credit with remark
        if remark != "" and acc != "" and cr_dr == "credit":
            try:
                
                acc = Account.objects.get(remark=acc,is_acc=True)
                acc.amount += int(amt)
                acc.save()
                a1 = Account.objects.create(remark=remark,amount= amt, check= False,date=date,is_acc =False)
                a1.save()
            except:
                messages.warning(request,"First create this account without remark")
          
        #withdarawal without remark      
        if remark == "" and acc != "" and cr_dr == "debit":
             messages.warning(request,"Remark is neccessary while debitting")
             return redirect("account")
        
        
        # withdrawal with remark      
        if remark != "" and acc != "" and cr_dr == "debit":
            try:
                acc = Account.objects.get(remark=acc,is_acc=True)
                acc.amount -= int(amt)
                acc.save()
                a1 = Account.objects.create(remark=remark,amount= amt, check= True,date=date,is_acc =False)
                a1.save()
            except:
                messages.success(request,"First create this account")
           
                
        
            
            
        return redirect('account')
    context={'items':a1,"amt":var1}
    return render(request,"registration/account.html",context)


def chck_amt(php,ptype):
    b = False
    tt_qty=0
    
    amt = getAmount(ptype)
    for i in php:
        tt_qty += i.price
    if tt_qty > amt:
        b = False
    else:
        b= True
    return b
        


@login_required(login_url='login')
def due_paid(request,id):
    if request.POST:
        ptype = request.POST.get('ptype')
        purObj = Purchase.objects.get(id=id)
        total=0
        php = PurchaseHasProduct.objects.filter(purchase=purObj)
        tf = chck_amt(php,ptype)
        if tf == False:
            messages.warning(request,"Due can not be paid ,insufficient balance")
            return redirect("purchase") 
        else:
            for i in php:
                a1 = Account.objects.create(date=datetime.now(),amount=i.price,remark=f"Purchase of  {i.product} from { purObj.supp } Due paid! ",check=True)
                a1.save()
                a2 = Account.objects.get(remark=ptype,is_acc=True)
                a2.amount -= i.price
                a2.save()
        purObj.payment_type = ptype
        purObj.save()
        messages.success(request,"Due paid")
        return redirect("purchase")
        

def freeReg(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            u1 = form.save(commit=False)
            u1.is_superuser = True
            u1.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            #login(request, user)
            return redirect('freeReg')
    else:
        form = UserCreationForm()
    return render(request,"registration/freeReg.html",{'form': form})
    return HttpResponse("hello")



def GetImei(request):
    prod = PurchaseHasProduct.objects.get(id=request.GET['id'])
    imei = prod.imei_no
    return JsonResponse(imei,safe=False)
    
def images(request):
    if request.method == "GET":
        imgs = ProductHasImg.objects.all()
        context={'imgs':imgs}
        return render(request,"registration/imgs.html",context)
    return render(request,"registration/imgs.html")
        
    
#for i in php:
#            total += i.price
#            if total < amt:
#                continue
#            else:
#                messages.warning(request,"Due can not be paid ,insufficient balance")
#                return redirect("purchase")  


 #     purObj = Purchase.objects.filter(date=datetime.today())
#     pur_prodObj = PurchaseHasProduct.objects.all()

#     salesObj = Sales.objects.filter(date=datetime.today())
    #     sales_prodObj = SalesHasProduct.objects.all()
    #     pcnt = purObj.count()
    #     scnt = salesObj.count()

    #     total = 0
    #     for i in purObj:
    #         for 
    #             if i == sp.purchase:sp in pur_prodObj:
    #                 total += (sp.price)
    #     total1=0
    #     for j in salesObj:
    #         for sp in sales_prodObj:
    #             if j == sp.sales:
    #                 total1 += (sp.price)
# pur':purObj,'php':pur_prodObj,'sale':salesObj,'shp':sales_prodObj,'total': total,'total1':total1,'pcnt':pcnt,'scnt':scnt

#   {% if total < total1 %}
#            <!-- <h3 class="bld">Profit:</h3><h4>{{ total1|sub:total }}</h4>-->
#         {% else %}
#         <!--<h3 class="bld">Loss:</h3><h4>{{ total|sub:total1 }}</h4>-->
#         {% endif %}