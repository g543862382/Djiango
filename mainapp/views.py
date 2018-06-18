import hashlib
import random
import uuid

import os
from datetime import time

from PIL import ImageFont, ImageDraw, Image
from django.db.models import Sum, F
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO

from AXF_project  import settings
from mainapp.models import TopWheel, TopMenu, Shop, MustBuy, MainShow, MainShowBrand, FondType, Goods, User, Cart, \
    DeliveryAddress, Order, OrderGoods


def home(req):
    shopList = Shop.objects.all().order_by('position')
    shop1 = shopList[0]
    shop2 = shopList[1:3]
    shop3 = shopList[3:7]
    shop4 = shopList[7:11]

    return render(req, "home.html",
                  {"title": "主页",
                   "topWheels": TopWheel.objects.all(),
                   "topMenus": TopMenu.objects.all().order_by('position'),
                   "mustbuys": MustBuy.objects.all(),
                   "shop1": shop1,
                   "shop2": shop2,
                   "shop3": shop3,
                   "shop4": shop4,
                   "mainShows": MainShowBrand.objects.all()})


def market(req, categoryid=0, childid=0, sortid=0):
    goodsList = None

    sortColumn = 'productid'  # 设置排序的列
    if sortid == 1:
        sortColumn = '-price'  # 价格最高
    elif sortid == 2:
        sortColumn = 'price'  # 价格最低
    elif sortid == 3:
        sortColumn = '-productnum'  # 销量最高

    # 获取所有子类型
    childTypes = []

    if categoryid:
        # 获取所有的子类型
        # 全部分类:0#酸奶乳酸菌:103537#牛奶豆浆:103538#面包蛋糕:103540
        cTypes = FondType.objects.filter(typeid=categoryid).last().childtypenames
        cTypes = cTypes.split('#')
        for ctype in cTypes:
            ctype = ctype.split(":")
            childTypes.append({"name": ctype[0], "id": ctype[1]})

        if childid:
            goodsList = Goods.objects.filter(categoryid=categoryid, childcid=childid).order_by(sortColumn)
        else:
            goodsList = Goods.objects.filter(categoryid=categoryid).order_by(sortColumn)
    else:
        goodsList = Goods.objects.all().order_by(sortColumn)[0:20]

    return render(req, 'market.html',
                  {'title': '闪购',
                   "foodTypes": FondType.objects.all().order_by('typesort'),
                   'goodsList': goodsList,
                   'categoryid': str(categoryid),
                   'childTypes': childTypes,
                   'childid': str(childid),
                   'sortid': sortid})


def mine(req):
    if not req.COOKIES.get('token'):
        return render(req,'login.html')

    return render(req, 'mine.html',
                  {'navs': getMyOrderNav(),
                   'menus': getMyOrderMenu(),
                   'loginUser': User.objects.filter(token=req.COOKIES.get('token')).first()})


def getMyOrderNav():
    navs = []
    navs.append({'name': '待付款', 'icon': 'glyphicon glyphicon-usd', 'url': '#'})
    navs.append({'name': '待收货', 'icon': 'glyphicon glyphicon-envelope', 'url': '#'})
    navs.append({'name': '待评价', 'icon': 'glyphicon glyphicon-pencil', 'url': '#'})
    navs.append({'name': '退款/售后', 'icon': 'glyphicon glyphicon-retweet', 'url': '#'})

    return navs


def getMyOrderMenu():
    menus = []
    menus.append({'name': '积分商城', 'icon': 'glyphicon glyphicon-bullhorn', 'url': '#'})
    menus.append({'name': '优惠券', 'icon': 'glyphicon glyphicon-credit-card', 'url': '#'})
    menus.append({'name': '收货地址', 'icon': 'glyphicon glyphicon-import', 'url': '#'})
    menus.append({'name': '客服/反馈', 'icon': 'glyphicon glyphicon-phone-alt', 'url': '#'})
    menus.append({'name': '关于我们', 'icon': 'glyphicon glyphicon-asterisk', 'url': '#'})

    return menus

def newToken(userName):
    # uuid + 用户名
    md5 = hashlib.md5()
    md5.update((str(uuid.uuid4())+userName).encode())
    return md5.hexdigest()

def crypt(pwd, cryptName='md5'):
    md5 = hashlib.md5()
    md5.update(pwd.encode())
    return md5.hexdigest()


def register(req):
    if req.method == 'GET':
        return render(req, 'register.html')

    user = User()
    user.userName = req.POST.get('username')
    user.userPasswd = crypt(req.POST.get('passwd'))
    user.phone = req.POST.get('phone')
    user.nickName = req.POST.get('nickname')

    # 设置用户的token
    user.token = newToken(user.userName)
    user.save()

    #将token设置到cookie中
    resp = render(req, 'mine.html', {'loginUser': user , 'navs': getMyOrderNav(),
                   'menus': getMyOrderMenu()})
    resp.set_cookie('token', user.token)

    return resp


@csrf_exempt  # 不做csrf_token验证
def upload(req):
    msg = {}
    cookie_token = req.COOKIES.get('token')
    if not cookie_token:
        msg['state'] = 'fail'
        msg['msg'] = '请先登录'
        msg['code'] = '201'
    else:
        qs = User.objects.filter(token=cookie_token)
        if not qs.exists():
            msg['state'] = 'fail'
            msg['msg'] = '登录失效，请重新登录'
            msg['code'] = '202'
        else:
            # 开始上传
            uploadFile = req.FILES.get('img')

            saveFileName = newFileName(uploadFile.content_type)
            saveFilePath = os.path.join(settings.MEDIA_ROOT, saveFileName)

            # 将上传文件的数据分段写入到目标文件（存放到当前服务端）中
            with open(saveFilePath, 'wb') as f:
                for part in uploadFile.chunks():
                    f.write(part)
                    f.flush()

            # 将上传文件的路径更新到用户
            qs.update(imgPath='upload/'+saveFileName)

            msg['state'] = 'ok'
            msg['msg'] = '上传成功'
            msg['code'] = '200'
            msg['path'] = 'upload/'+saveFileName

    return JsonResponse(msg)


def newFileName(contentType):
    fileName = crypt(str(uuid.uuid4()))
    extName = '.jpg'
    if contentType == 'image/png':
        extName  = '.png'

    return fileName+extName


def cart(req):
    # 查询当前用户的默认收货信息
    user_id = req.session.get('user_id')
    if not user_id:
        return render(req,'login.html',{'title':'用户登陆'})
    deliveryAddresee = DeliveryAddress.objects.filter(user_id=user_id).first()
    carts = Cart.objects.filter(user_id=user_id)
    totalPrice = 0
    for cart in carts:
        if cart.isSelected:
            totalPrice += cart.goods.price*cart.cnt
    return render(req,'cart.html',{'title':'购物车',
                                   'myAddress':deliveryAddresee,
                                   'carts':carts,
                                    'totalPrice':totalPrice})


def logout(req):
    resp = render(req,'login.html')
    if req.COOKIES.get('token'):
        # 解除和用户绑定的token
        User.objects.filter(token=req.COOKIES.get('token')).update(token='')

        # 从Cookie中删除
        resp.delete_cookie('token')

        # 从session中删除user_id
        del req.session['user_id']

    return resp

def login(req):
    if req.method == 'GET':
        return render(req, 'login.html')

    username = req.POST.get('username')
    passwd = req.POST.get('passwd')

    qs = User.objects.filter(userName=username,
                             userPasswd=crypt(passwd))
    if qs.exists():
            user = qs.first()
            req.session['user_id'] = user.id
            user.token = newToken(user.userName)
            user.save()
            resp = render(req,'mine.html',{'user':user})
            resp.set_cookie('token',user.token)
            return resp
    else:
            return render(req,'login.html',{'error_msg':'用户登陆失败，请重试'})

def verifycode(req):
    # 1. 创建画布Image对象
    img = Image.new(mode='RGB', size=(120, 30), color=(220, 220, 180))

    # 2. 创建画笔 ImageDraw对象
    draw = ImageDraw.Draw(img, 'RGB')

    # 3. 画文本，画点，画线
    # 随机产生0-9, A-Z, a-z范围的字符
    chars = ''
    while len(chars) < 4:
        flag = random.randrange(3)
        char = chr(random.randint(48, 57)) if not flag else \
                  chr(random.randint(65, 90)) if flag == 1 else \
                  chr(random.randint(97, 122))
        # 排除重复的
        if len(chars) == 0 or chars.find(char) == -1:
            chars += char

    # 将生成的验证码的字符串存入到session中
    req.session['verifycode'] = chars

    font = ImageFont.truetype(font='static/fonts/hktt.ttf', size=25)
    for char in chars:
        xy = (15+chars.find(char)*20, random.randrange(2, 8))
        draw.text(xy=xy,
                  text=char,
                  fill=(255, 0, 0),
                  font=font)
    for i in range(200):
        xy = (random.randrange(120), random.randrange(30))
        color = (random.randrange(255),
                 random.randrange(255),
                 random.randrange(255))
        draw.point(xy=xy, fill=color)

    # 4. 将画布对象转成字节数据
    buffer = BytesIO()  # 缓存
    img.save(buffer, 'png')  # 指定的图片格式为png

    # 5. 清场(删除对象的引用)
    del draw
    del img
    return HttpResponse(buffer.getvalue(),  # 从BytesIO对象中获取字节数据
                        content_type='image/png')


def selectCart(req,cart_id):
    if cart_id == 0 or cart_id == 99999:
        carts = Cart.objects.filter(user_id=req.session.get('user_id'))
        carts.update(isSelected = True if cart_id == 0 else False)
        totalPrice = 0
        if cart_id == 0:
            for cart in carts:
                totalPrice += cart.cnt * cart.goods.price
        return JsonResponse({'price':totalPrice,
                             'status':200})

    data = {'status':200,'price':1000.5}
    try:
        cart = Cart.objects.get(id = cart_id)
        cart.isSelected = not cart.isSelected
        cart.save()
        data['price'] = cart.cnt*cart.goods.price
        data['selected'] = cart.isSelected
    except:
        data['status'] = 300
        data['price'] = 0

    return JsonResponse(data)


def addCart(req, cart_id):
    # 添加指定cart_id的商品 cnt，如果cart_id不存在时，要新添加？
    price = 0
    qs = Cart.objects.filter(id=cart_id)
    if qs.exists():
        price = qs.first().goods.price
        qs.update(cnt=F('cnt') + 1)

    else:
        # 如果在Cart中查找不到，则表示cart_id为goods_id
        user_id = req.session.get('user_id');
        qs = Cart.objects.filter(user_id=user_id, goods_id=cart_id)
        if qs.exists():
            qs.update(cnt=F('cnt') + 1)
        else:
            qs.create(user_id=user_id, goods_id=cart_id, cnt=1)

        # 查看商品的单价
        price = Goods.objects.filter(productid=cart_id).first().price

    return JsonResponse({'status': 200,
                         'price': price,
                         'msg': '添加或更新购物车成功!'})


def subCart(req, cart_id):
    # 减去 指定cart_id的商品的cnt, 如果cnt为0时，要删除？
    price = 0
    data = {'status': 200, 'price': '10'}
    qs = Cart.objects.filter(id=cart_id)
    if qs.exists():
        price = qs.first().goods.price
        if qs.first().cnt > 0:
            qs.update(cnt=F('cnt') - 1)
            data['price'] = price
        else:
            data['price'] = '0'
            data['status'] = 201  # 不能再减了
    else:
        data['price'] = '0'
        data['status'] = 300  # 不存在

    return JsonResponse(data)


def createOrderNum():
    orderNum = '0029'+str(time.time()).replace(',','')[-10:]
    return orderNum

def order(req,num):
    user_id = req.session.get('user_id')
    if not user_id:
        return render(req,'login.html')
    order = None
    if num == 0:
        # 下订单
        order = Order()
        order.user_id = user_id()
        #h获取用户的第一个收货地址，作为第一个地址
        order.orderAddress_id = User.objects.get(pk = user_id).deliveryaddress_set.first().pk
        # 设置订单号
        order.orderNum = createOrderNum()
        # 1 .查询当前用户下的购物车中所有选择的商品
        carts = Cart.objects.filter(isSelected=True ,user_id = user_id)
        if carts.count() == 0:
            return HttpResponseRedirect('/app/cart')
        order.save()
        # 2. 统计订单总金额 和 将商品插入到订单明细中
        order.orderPrice = 0
        for cart in carts:
            order.orderPrice += cart.cnt * cart.goods.price
            ordergoods = OrderGoods()
            ordergoods.order_id = order.orderNum
            ordergoods.goods_id = cart.goods.pk
            ordergoods.cnt = cart.cnt
            ordergoods.price = cart.cnt * cart.goods.price
            ordergoods.save()
            #保存订单
            order.save()
            carts.delete() #删除购物车里已选购的商品
    else:
        order = Order.objects.get( pk = num )
    return render(req,'order.html',{'title':'我的订单',
                                       'order':order})


def pay(req,num,payType):
    try:
        order = Order.objects.get(pk=num)
        order.payType = payType
        user = User.objects.get(pk=req.session.get('user_id'))
        if user.money < order.orderPrice:
            return JsonResponse({'status':'fail',
                                 'msg':'余款不足'})
        else:
            user.monry -= order.orderPrice
            user.save()
            order.payState = 1
            order.save()
            for item in order.ordergoods_set.all():
                goods = item.goods
                goods.productnum +=item.cnt
                goods.storenums -= item.cnt
                goods.save()
    except:
        return JsonResponse({'status':'fail',
                             'msg':'支付失败！'})
    return JsonResponse({'status':'ok',
                         'msg':'支付成功！'})
