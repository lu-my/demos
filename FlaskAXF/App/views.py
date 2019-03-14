import os
from flask import Blueprint, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from App.ext import photos, db
from App.models import AXFUser, MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods
from App.views_constant import ALL_TYPE, ORDER_TOTAL, ORDER_PRICE_UP, ORDER_PRICE_DOWN, ORDER_SALE_UP, ORDER_SALE_DOWN

blue = Blueprint('blue', __name__)
destination = os.path.dirname(os.path.abspath(__file__)) + '/static/uploads/icons/PHOTO/'


def init_views(app):
    app.register_blueprint(blue)


@blue.route('/hello/')
def hello_world():
    return 'Hello World!'


@blue.route('/home/')
def home():
    main_wheels = MainWheel.query.all()
    main_navs = MainNav.query.all()
    main_mustbuys = MainMustBuy.query.all()
    main_shops = MainShop.query.all()
    main_shop0_1 = main_shops[0:1]
    main_shop1_3 = main_shops[1:3]
    main_shop3_7 = main_shops[3:7]
    main_shop7_11 = main_shops[7:11]
    main_shows = MainShow.query.all()

    return render_template('main/home.html', main_wheels=main_wheels, main_navs=main_navs, main_mustbuys=main_mustbuys,
                           main_shops=main_shops, main_shop0_1=main_shop0_1, main_shop1_3=main_shop1_3,
                           main_shop3_7=main_shop3_7, main_shop7_11=main_shop7_11,
                           main_shows=main_shows)


@blue.route('/market/')
def market():
    return redirect(url_for('blue.market_with_params', typeid=104749, childid=0, order_rule=0))


@blue.route('/market_with_params/<string:typeid>/<string:childid>/<string:order_rule>')
def market_with_params(typeid, childid, order_rule):
    print(typeid, childid, order_rule)
    food_types = FoodType.query.all()  # list对象
    goods_list = Goods.query.filter(Goods.categoryid.__eq__(typeid))  # BaseQuery对象
    print("----------", goods_list.all())

    # 子类型筛选
    if childid == ALL_TYPE:
        pass
    else:
        goods_list = goods_list.filter(Goods.childcid.__eq__(childid))  # BaseQuery对象

    print("----------", goods_list.all())
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
    print("----------", goods_list.all())
    # type_total = food_types.get(typeid=typeid)
    type_total = FoodType.query.filter(FoodType.typeid.__eq__(typeid)).first()
    print("type_total:", type_total)

    child_type_names = type_total.childtypenames.split("#")
    print("child_type_names:", child_type_names)
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
    title = "闪送超市"
    food_types = food_types
    print("food_types:", food_types)
    goods_list = goods_list.all()
    print("goods_list", goods_list)
    typeid = int(typeid)
    print("typeid:", typeid)
    child_types = child_types
    print("child_types:", child_types)
    order_rule_list = order_rule_list
    print("order_rule_list:", order_rule_list)
    childid = childid
    print("childid:", childid)

    return render_template('main/market.html', title=title, food_types=food_types, goods_list=goods_list, typeid=typeid,
                           child_types=child_types, order_rule_list=order_rule_list, childid=childid)


@blue.route('/cart/')
def cart():
    pass


@blue.route('/mine/')
def mine():
    title = "我的"
    is_login = False

    if request.user:
        user = request.user
        is_login = True
        username = user.u_username
        icon = destination + user.u_icon
        # data['order_not_pay'] = Order.objects.filter(o_user=user).filter(o_status=ORDER_STATUS_NOT_PAY).count()
        # data['order_not_receive'] = Order.objects.filter(o_user=user).filter(
        #     o_status__in=[ORDER_STATUS_NOT_RECEIVE, ORDER_STATUS_NOT_SEND]).count()
        return render_template('main/mine.html', title=title, is_login=is_login, username=username, icon=icon)
    else:
        return render_template('user/login.html')


@blue.route('/register/', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('user/register.html')
    elif request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        filename = photos.save(request.files['icon'])

        print(password)
        user = AXFUser()
        user.u_username = name
        user.u_email = email
        user.u_password = generate_password_hash(password)
        user.u_icon = filename

        db.session.add(user)
        db.session.commit()

        return 'register success'


@blue.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('user/login.html')
    elif request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        print(password)

        user = AXFUser.query.filter(AXFUser.u_username.__eq__(name)).first()  # 找不到返回None
        if user:
            if check_password_hash(user.u_password, password):
                session["user_id"] = user.id
                print(session.get("user_id"))
                print("登陆成功")
                return redirect(url_for('blue.mine'))
            else:
                return 'password error'
        return 'user dose not exist'


@blue.route('/logout/')
def logout():
    return 'logout'
