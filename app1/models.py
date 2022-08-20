from django.db import models
# Create your models here.

class Supplier(models.Model):
    supp_name = models.CharField(max_length=40)
    phone = models.IntegerField(null=False)

    def __str__(self):
        return self.supp_name

class Purchase(models.Model):
    date = models.DateField(null=True)
    supp = models.ForeignKey(Supplier,on_delete=models.DO_NOTHING)
    payment_type = models.CharField(max_length=50)

class PurchaseHasProduct(models.Model):
    purchase =  models.ForeignKey(Purchase,on_delete=models.CASCADE)
    product = models.CharField(max_length=40)
    imei_no     = models.BigIntegerField()
    price     = models.IntegerField()
    pur_prod = models.BooleanField(default=False)

    def __str__(self):
        return self.product+' '+str(self.imei_no)


class Sales(models.Model):
    date = models.DateField(null=True)
    customer = models.CharField(max_length=40)
    phone   = models.IntegerField(null=True)

    def __str__(self):
        return str(self.id)

class SalesHasProduct(models.Model):
    sales = models.ForeignKey(Sales,on_delete=models.DO_NOTHING)
    product = models.ForeignKey(PurchaseHasProduct,on_delete=models.DO_NOTHING)
    imei_no = models.BigIntegerField(null=True)
    price = models.IntegerField()


class Account(models.Model):
    date = models.DateTimeField(default=None)
    amount = models.IntegerField(null=True)
    remark =  models.CharField(max_length=50)
    check = models.BooleanField(default=False)
    is_acc = models.BooleanField(default=False)
    
    
class ProductHasImg(models.Model):
	img = models.ImageField(upload_to='my_img',  max_length=100)
	prod     =  models.ForeignKey(PurchaseHasProduct,on_delete=models.CASCADE)
	
    






    
      