import uuid

from alipay import AliPay
from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from AXF.settings import MEDIA_KEY_PREFIX, ALIPAY_APPID, APP_PRIVATE_KEY, ALIPAY_PUBLIC_KEY
from App.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods, AXFUser, Cart, Order, \
    OrderGoods, Address, OrderAddress
from App.views_constant import ORDER_TOTAL, ORDER_PRICE_UP, ORDER_PRICE_DOWN, ORDER_SALE_UP, ORDER_SALE_DOWN, ALL_TYPE, \
    HTTP_OK, HTTP_USER_EXIST, ORDER_STATUS_NOT_PAY, ORDER_STATUS_NOT_RECEIVE, ORDER_STATUS_NOT_SEND
from App.views_helper import get_total_price, send_email_activate


def home(request):
    main_wheels = MainWheel.objects.all()
    main_navs = MainNav.objects.all()
    main_mustbuys = MainMustBuy.objects.all()
    main_shops = MainShop.objects.all()
    main_shop0_1 = main_shops[0:1]
    main_shop1_3 = main_shops[1:3]
    main_shop3_7 = main_shops[3:7]
    main_shop7_11 = main_shops[7:11]
    main_shows = MainShow.objects.all()
    data = {
        'title': "首页",
        'main_wheels': main_wheels,
        'main_navs': main_navs,
        'main_mustbuys': main_mustbuys,
        'main_shop0_1': main_shop0_1,
        'main_shop1_3': main_shop1_3,
        'main_shop3_7': main_shop3_7,
        'main_shop7_11': main_shop7_11,
        'main_shows': main_shows,
    }
    return render(request, 'main/home.html', context=data)


def market(request):
    return redirect(reverse('axf:market_with_params', kwargs={
        'typeid': 104749,
        'childid': 0,
        'order_rule': 0,
    }))


def market_with_params(request, typeid, childid, order_rule):
    '''

    :param request:
    :param typeid: 左侧大类型
    :param childid: 子类型
    :param order_rule: 排序规则
    :return:
    '''
    print(typeid, childid, order_rule)
    food_types = FoodType.objects.all()
    goods_list = Goods.objects.all().filter(categoryid=typeid)

    # 子类型筛选
    if childid == ALL_TYPE:
        pass
    else:
        goods_list = goods_list.filter(childcid=childid)

    # 排序
    if order_rule == ORDER_TOTAL:
        pass
    elif order_rule == ORDER_PRICE_UP:
        goods_list = goods_list.order_by("price")
    elif order_rule == ORDER_PRICE_DOWN:
        goods_list = goods_list.order_by("-price")
    elif order_rule == ORDER_SALE_UP:
        goods_list = goods_list.order_by("productnum")
    elif order_rule == ORDER_SALE_DOWN:
        goods_list = goods_list.order_by("-productnum")

    type_total = food_types.get(typeid=typeid)
    child_type_names = type_total.childtypenames.split("#")
    child_types = []
    for child_type_name in child_type_names:
        child_type = child_type_name.split(":")
        child_types.append(child_type)

    order_rule_list = [
        ['综合排序', ORDER_TOTAL],
        ['价格升序', ORDER_PRICE_UP],
        ['价格降序', ORDER_PRICE_DOWN],
        ['销量升序', ORDER_SALE_UP],
        ['销量降序', ORDER_SALE_DOWN],
    ]
    data = {
        'title': "闪送超市",
        'food_types': food_types,
        'goods_list': goods_list,
        'typeid': int(typeid),
        'child_types': child_types,
        'order_rule_list': order_rule_list,
        'childid': childid,

    }
    return render(request, 'main/market.html', context=data)


def cart(request):
    user = request.user
    print(user.id)
    carts = Cart.objects.filter(c_user=user)

    address = Address.objects.filter(a_using=True).first()

    data = {
        'title': "购物车",
        'carts': carts,
        "address": address,
        "name": user.u_username
    }
    return render(request, 'main/cart.html', context=data)


def mine(request):
    user_id = request.session.get("user_id")
    data = {
        'title': "我的",
        'is_login': False,
    }

    if user_id:
        user = AXFUser.objects.get(pk=user_id)
        data['is_login'] = True
        data['username'] = user.u_username
        data['icon'] = MEDIA_KEY_PREFIX + user.u_icon.url
        data['order_not_pay'] = Order.objects.filter(o_user=user).filter(o_status=ORDER_STATUS_NOT_PAY).count()
        data['order_not_receive'] = Order.objects.filter(o_user=user).filter(
            o_status__in=[ORDER_STATUS_NOT_RECEIVE, ORDER_STATUS_NOT_SEND]).count()
    return render(request, 'main/mine.html', context=data)


def register(request):
    if request.method == 'GET':
        data = {
            'title': '注册',
        }
        return render(request, 'user/register.html', context=data)
    elif request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        icon = request.FILES.get("icon")

        user = AXFUser()
        user.u_username = name
        user.u_email = email
        user.u_password = make_password(password)
        user.u_icon = icon
        user.save()

        # 发送激活邮件
        u_token = uuid.uuid4().hex

        cache.set(u_token, user.id, timeout=60 * 60 * 24)

        send_email_activate(name, email, u_token)

        return render(request, 'user/login.html')


def activate(request):
    u_token = request.GET.get('u_token')

    user_id = cache.get(u_token)

    if user_id:
        cache.delete(u_token)

        user = AXFUser.objects.get(pk=user_id)

        user.is_active = True

        user.save()

        return redirect(reverse('axf:login'))

    return render(request, 'user/activate_fail.html')


def login(request):
    if request.method == 'GET':
        data = {
            'title': '登陆',
        }
        return render(request, 'user/login.html', context=data)
    elif request.method == "POST":
        name = request.POST.get("name")
        password = request.POST.get("password")
        try:
            users = AXFUser.objects.filter(u_username=name)
            if users.exists():
                user = users.first()
                if check_password(password, user.u_password):
                    if user.is_active:
                        request.session['user_id'] = user.id
                        return redirect(reverse('axf:mine'))
                    else:
                        print('not activate')
                        request.session['error_message'] = 'not activate'
                        return redirect(reverse('axf:login'))
                else:
                    print("密码错误")
                    request.session['error_message'] = 'password error'
                    return redirect(reverse('axf:login'))
            else:
                print("用户不存在")
                request.session['error_message'] = 'user does not exist'
                return redirect(reverse('axf:login'))
        except Exception as e:
            print(e)
            return HttpResponse("chengong")
            # return redirect(reverse('axf:login'))


def file_modify(request):
    if request.method == 'GET':
        user_name = request.session["username"]
        user = AXFUser.objects.get(u_username=user_name)
        icon_url = "/static/uploads/" + user.u_icon.url
        data = {
            'title': '个人资料',
            'user': user,
            'icon_url': icon_url,
        }
        return render(request, 'user/file_modify.html', context=data)
    elif request.method == "POST":
        name = request.session["username"]
        new_name = request.POST.get("new_name")
        new_email = request.POST.get("new_email")
        password = request.POST.get("password")
        new_password = request.POST.get("new_password")
        new_icon = request.FILES.get("new_icon")

        try:
            user = AXFUser.objects.get(u_username=name)
            if not check_password(password, user.u_password):
                return HttpResponse("密码错误")
            user.u_username = new_name
            user.u_email = new_email
            user.u_password = make_password(new_password)
            user.u_icon = new_icon
            user.save()
            icon_url = "/static/uploads/" + user.u_icon.url
            data = {
                'user': user,
                'icon_url': icon_url,
            }
            return render(request, 'user/file_modify.html', context=data)
        except Exception:
            return HttpResponse("用户不存在")


def check_user(request):
    name = request.GET.get("name")
    users = AXFUser.objects.filter(u_username=name)
    data = {
        "status": HTTP_OK,
        "msg": 'user can use'
    }
    if users.exists():
        data['status'] = HTTP_USER_EXIST
        data['msg'] = 'user already exist'
    else:
        pass
    return JsonResponse(data=data)


def add_to_cart(request):
    goodsid = request.GET.get('goodsid')
    user_id = request.session.get("user_id")
    carts = Cart.objects.filter(c_user_id=user_id).filter(c_goods_id=goodsid)
    if carts.exists():
        cart_obj = carts.first()
        cart_obj.c_goods_num = cart_obj.c_goods_num + 1
    else:
        cart_obj = Cart()
        cart_obj.c_user_id = user_id
        cart_obj.c_goods_id = goodsid

    cart_obj.save()

    data = {
        'status': 200,
        'msg': 'add succcess',
        'c_goods_num': cart_obj.c_goods_num,
    }
    return JsonResponse(data)


def logout(request):
    request.session.flush()
    return redirect(reverse('axf:mine'))


def sub_shopping(request):
    cartid = request.GET.get('cartid')
    cart_obj = Cart.objects.get(pk=cartid)

    data = {
        'status': 200,
        'msg': 'ok',
    }
    if cart_obj.c_goods_num > 1:
        cart_obj.c_goods_num = cart_obj.c_goods_num - 1
        cart_obj.save()
        data['c_goods_num'] = cart_obj.c_goods_num
    else:
        cart_obj.delete()
        data['c_goods_num'] = 0

    return JsonResponse(data)


def add_shopping(request):
    cartid = request.GET.get('cartid')

    data = {
        'status': 200,
        'msg': 'ok',
    }
    try:
        cart_obj = Cart.objects.get(pk=cartid)
        cart_obj.c_goods_num = cart_obj.c_goods_num + 1
        cart_obj.save()
        data["c_goods_num"] = cart_obj.c_goods_num,
    except:
        pass

    return JsonResponse(data)


def change_cart_state(request):
    cartid = request.GET.get('cartid')
    data = {
        'status': 200,
        'msg': 'ok',
    }
    try:
        cart_obj = Cart.objects.get(pk=cartid)
        cart_obj.c_is_select = not cart_obj.c_is_select
        cart_obj.save()
        data["c_is_select"] = cart_obj.c_is_select
        is_all_selected = not Cart.objects.filter(c_user=request.user).filter(c_is_select=False).exists()
        print(is_all_selected)
        print(type(is_all_selected))
        data["is_all_selected"] = is_all_selected
    except Exception as e:
        print(e)
    return JsonResponse(data)


def all_select(request):
    cart_list = request.GET.get('cart_list')
    cart_list = cart_list.split("#")

    carts = Cart.objects.filter(pk__in=cart_list)

    for cart_obj in carts:
        cart_obj.c_is_select = not cart_obj.c_is_select
        cart_obj.save()
    data = {
        'status': 200,
        'msg': 'ok',
    }
    return JsonResponse(data)


def order_detail(request):
    order_id = request.GET.get("order_id")

    order = Order.objects.get(pk=order_id)
    data = {
        'title': "订单详情",
        "order": order,
    }
    return render(request, 'order/order_detail.html', context=data)


def make_order(request):
    carts = Cart.objects.filter(c_user=request.user).filter(c_is_select=True)

    order = Order()
    order.o_user = request.user
    order.o_price = get_total_price()
    order.save()

    for cart_obj in carts:
        ordergoods = OrderGoods()
        ordergoods.o_order = order
        ordergoods.o_goods_num = cart_obj.c_goods_num
        ordergoods.o_goods = cart_obj.c_goods
        ordergoods.save()
        # 从购物车中删除
        cart_obj.delete()

    address_obj = Address.objects.filter(a_user=request.user).filter(a_using=True).first()
    order_address_obj = OrderAddress()
    order_address_obj.oa_address = address_obj
    order_address_obj.oa_order = order
    order_address_obj.save()
    data = {
        "status": 200,
        "msg": "ok",
        "order_id": order.id,
    }
    return JsonResponse(data)


def order_list_not_pay(request):
    orders = Order.objects.filter(o_user=request.user).filter(o_status=ORDER_STATUS_NOT_PAY)
    data = {
        "orders": orders,
    }

    return render(request, 'order/order_list_not_pay.html', context=data)


def payed(request):

    orderid = request.GET.get("out_trade_no")

    order = Order.objects.get(pk=orderid)
    order.o_status = ORDER_STATUS_NOT_SEND
    order.save()

    print("支付成功")
    # return HttpResponse("支付成功")
    return redirect(reverse('axf:mine'))


def order_list_not_receive(request):
    orders = Order.objects.filter(o_user=request.user).filter(
        o_status__in=[ORDER_STATUS_NOT_RECEIVE, ORDER_STATUS_NOT_SEND])

    data = {
        'title': "待收货",
        'orders': orders,

    }
    return render(request, 'order/order_list_not_receive.html', context=data)


def alipay(request):
    # 构建支付的科幻  AlipayClient
    alipay_client = AliPay(
        appid=ALIPAY_APPID,
        app_notify_url=None,  # 默认回调url
        app_private_key_string=APP_PRIVATE_KEY,
        alipay_public_key_string=ALIPAY_PUBLIC_KEY,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA",  # RSA 或者 RSA2
        debug=False  # 默认False
    )
    # 使用Alipay进行支付请求的发起

    subject = request.GET.get("subject")
    total_price = request.GET.get("total_price")
    order_id = request.GET.get("order_id")


    # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
    order_string = alipay_client.api_alipay_trade_page_pay(
        out_trade_no=order_id,
        total_amount=total_price,
        subject=subject,
        return_url="http://127.0.0.1:8000/axf/payed/",
        notify_url="http://127.0.0.1:8000/axf/payed/"  # 可选, 不填则使用默认notify url
    )

    # 客户端操作
    url = "https://openapi.alipaydev.com/gateway.do?" + order_string
    data = {
        "status": 200,
        "msg": "ok",
        "url": url
    }
    return JsonResponse(data)


def address_list(request):

    add_list = Address.objects.filter(a_user=request.user)
    address_num = add_list.count()

    data = {
        "status": 200,
        "msg": "ok",
        "title": "选择收货地址",
        "add_list": add_list,
        "address_num": address_num,
    }

    return render(request, 'user/address_list.html', context=data)


def add_address(request):
    new_address = request.GET.get("new_address")

    print(new_address)

    address_obj = Address()
    address_obj.a_address = new_address
    address_obj.a_user = request.user
    address_obj.a_using = True
    address_obj.save()

    data = {
        "status": 200,
        "msg": "ok",

    }
    return JsonResponse(data)


def choose_address(request):
    address_id = request.GET.get("address_id")

    order_address_obj = OrderAddress()
    order_address_obj.oa_address_id = address_id
    order_address_obj.oa

    return None