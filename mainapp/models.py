from django.db import models
class TopModel(models.Model):
    trackid = models.CharField(primary_key=True, max_length=10)
    img = models.CharField(max_length=300)
    name = models.CharField(max_length=50)
    class Meta:
        abstract = True
# Create your models here.
class TopWheel(TopModel):
    class Meta:
        db_table = 'axf_wheel' #指定表面

class TopMenu(TopModel):
    position = models.IntegerField(default=1)
    class Meta:
        db_table = 'axf_nav' # 导航菜单
class MustBuy(TopModel):
    class Meta:
        db_table = 'axf_mustbuy'

class Shop(TopModel):
    position = models.IntegerField(default=1)
    class Meta:
        db_table='axf_shop'

class MainShow(models.Model):
    trackid = models.CharField(max_length=10)
    name = models.CharField(max_length=20)
    img = models.CharField(max_length=100)
    categoryid = models.CharField(max_length=10)
    brandname = models.CharField(max_length=20)

    img1 = models.CharField(max_length=100)
    childcid1 = models.CharField(max_length=10)
    productid1 = models.CharField(max_length=10)
    longname1 = models.CharField(max_length=50)
    price1 = models.CharField(max_length=10)
    marketprice1 = models.CharField(max_length=10)

    img2 = models.CharField(max_length=100)
    childcid2 = models.CharField(max_length=10)
    productid2 = models.CharField(max_length=10)
    longname2 = models.CharField(max_length=50)
    price2 = models.CharField(max_length=10)
    marketprice2 = models.CharField(max_length=10)

    img3 = models.CharField(max_length=100)
    childcid3 = models.CharField(max_length=10)
    productid3 = models.CharField(max_length=10)
    longname3 = models.CharField(max_length=50)
    price3 = models.CharField(max_length=10)
    marketprice3 = models.CharField(max_length=10)
    class Meta:
        db_table = 'axf_mainshow'
# 热购的品牌信息
class MainShowBrand(models.Model):
    trackid = models.CharField(max_length=10)
    img = models.CharField(max_length=300)
    name = models.CharField(max_length=50)

    categoryid = models.CharField(max_length=10)
    brandname = models.CharField(max_length=20)
    class Meta:
        db_table = 'axf_brand'
# 品牌下的商品
class BrandProduct(models.Model):
    img = models.CharField(max_length=100)
    childcid = models.CharField(max_length=10)
    productid = models.CharField(max_length=10)
    longname = models.CharField(max_length=50)
    price = models.CharField(max_length=10)
    marketprice = models.CharField(max_length=10)
    brand = models.ForeignKey(MainShowBrand,on_delete=models.CASCADE)
    class Meta:
        db_table = 'axf_brand_product'

class FondType(models.Model):
    typeid = models.CharField(primary_key=True,max_length=10)
    typename = models.CharField(max_length=50)
    childtypenames = models.CharField(max_length=200)
    typesort = models.IntegerField(default=1)

    class Meta:
        db_table = "axf_foodtypes"

class Goods(models.Model):
    productid = models.CharField(primary_key=True,max_length=10)
    productimg = models.CharField(max_length=300)
    productname = models.CharField(max_length=100)

    productlongname = models.CharField(max_length=100)
    isxf = models.BooleanField(default=1)
    pmdesc = models.IntegerField(default=1)
    specifics = models.CharField(max_length=100)
    price = models.DecimalField(default=0.0,max_digits=10,decimal_places=2)
    marketprice = models.DecimalField(default=0.0,max_digits=10,decimal_places=2)

    categoryid = models.IntegerField(default=0)
    childcid = models.IntegerField(default=0)
    childcidname = models.CharField(max_length=100)

    dealerid = models.CharField(max_length=20)
    storenums = models.IntegerField(default=1)
    productnum = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'axf_goods'

class UserManager(models.Manager):
    def get_queryset(self):
        super().get_queryset().filter(state=True)

class User(models.Model):
    userName = models.CharField(max_length=20)
    userPasswd = models.CharField(max_length=64)
    phone = models.CharField(max_length=12)
    adderss = models.CharField(max_length=100,default='')
    city = models.CharField(max_length=100,default='')
    nickName = models.CharField(max_length=50,verbose_name='昵称')

    imgPath = models.CharField(max_length=100,default='')

    token = models.CharField(max_length=32,default='')
    state = models.BooleanField(default=True,verbose_name='用户状态')

    object = UserManager

    def delete(self, using=None, keep_parents=False):
        self.state = False
        self.save()
        return '已注销'
    class Meta:
        db_table = 'axf_user'
class DeliveryAddress(models.Model):
    name = models.CharField(max_length=20,verbose_name='收件人')
    phone = models.CharField(max_length=12,verbose_name='电话')
    address_detail = models.TextField(default='',verbose_name='收货地址')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        db_table = 'axf_address'

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE)
    cnt = models.IntegerField(default=1)
    isSelected = models.BooleanField(default=True)

    class Meta:
        db_table = 'axf_cart'

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    orderAddress = models.ForeignKey(DeliveryAddress,on_delete=models.SET_NULL,null=True)
    order = models.CharField(primary_key=True,max_length=50,verbose_name='订单号')
    orderPrice = models.DecimalField(max_digits=10,decimal_places=2,default=0)

    pay_types = ((0,'余款'),(1,'支付宝'),(2,'微信'))
    payType = models.IntegerField(choices=pay_types,default=0)

    pay_states = ((0,'待支付'),(1,'已支付'),(2,'正在支付中'))
    payStates = models.IntegerField(choices=pay_states,default=0)
    @property
    def payStateName(self):
        return self.pay_states[self.payStates][1]

    order_states = ((0,'待派送'),(1,'已派送'),(2,'已到达'),(3,'已签收'),(4,'拒收'),(5,'未到达'))
    orderstates = models.IntegerField(choices=order_states,default=0)
    @property
    def orderStateName(self):
        return self.order_states[self.orderstates][1]

    orderTime = models.DateTimeField(auto_now_add=True)
    orderLastTime = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'axf_order'

class OrderGoods(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods,on_delete=models.SET_NULL,null=True)
    cnt = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2,default=0,verbose_name='小计')

    class Meta:
        db_table = 'axf_order_goods'