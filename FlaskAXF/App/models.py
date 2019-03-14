from App.ext import db


class AXFUser(db.Model):
    __tablename__ = 'axf_user'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    u_username = db.Column(db.String(32), unique=True)
    u_password = db.Column(db.String(256), unique=True)
    u_email = db.Column(db.String(64), unique=True)
    u_icon = db.Column(db.String(256), unique=True)
    is_active = db.Column(db.Boolean, default=False)
    is_delete = db.Column(db.Boolean, default=False)


class Main(db.Model):
    __abstract__ = True

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    img = db.Column(db.String(256))
    name = db.Column(db.String(64))
    trackid = db.Column(db.INTEGER, default=1)


class MainWheel(Main):
    __tablename__ = 'axf_wheel'



class MainNav(Main):
    __tablename__ = 'axf_nav'


class MainMustBuy(Main):
    __tablename__ = 'axf_mustbuy'


class MainShop(Main):
    __tablename__ = 'axf_shop'


class MainShow(Main):
    __tablename__ = 'axf_mainshow'

    categoryid = db.Column(db.INTEGER, default=1)
    brandname = db.Column(db.String(64))

    img1 = db.Column(db.String(255))
    childcid1 = db.Column(db.INTEGER, default=1)
    productid1 = db.Column(db.INTEGER, default=1)
    longname1 = db.Column(db.String(128))
    price1 = db.Column(db.Float, default=1)
    marketprice1 = db.Column(db.Float, default=0)

    img2 = db.Column(db.String(255))
    childcid2 = db.Column(db.INTEGER, default=1)
    productid2 = db.Column(db.INTEGER, default=1)
    longname2 = db.Column(db.String(128))
    price2 = db.Column(db.Float, default=1)
    marketprice2 = db.Column(db.Float, default=0)

    img3 = db.Column(db.String(255))
    childcid3 = db.Column(db.INTEGER, default=1)
    productid3 = db.Column(db.INTEGER, default=1)
    longname3 = db.Column(db.String(128))
    price3 = db.Column(db.Float, default=1)
    marketprice3 = db.Column(db.Float, default=0)


class FoodType(db.Model):
    __tablename__ = 'axf_foodtype'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    typeid = db.Column(db.INTEGER, default=1)
    typename = db.Column(db.String(32))
    childtypenames = db.Column(db.String(256))
    typesort = db.Column(db.INTEGER, default=1)


class Goods(db.Model):
    __tablename__ = 'axf_goods'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    productid = db.Column(db.INTEGER, default=1)
    productimg = db.Column(db.String(256))
    productname = db.Column(db.String(128))
    productlongname = db.Column(db.String(256))
    isxf = db.Column(db.Boolean, default=False)
    pmdesc = db.Column(db.Boolean, default=False)
    specifics = db.Column(db.String(64))
    price = db.Column(db.Float, default=0)
    marketprice = db.Column(db.Float, default=1)
    categoryid = db.Column(db.INTEGER, default=1)
    childcid = db.Column(db.INTEGER, default=1)
    childcidname = db.Column(db.String(128))
    dealerid = db.Column(db.INTEGER, default=1)
    storenums = db.Column(db.INTEGER, default=1)
    productnum = db.Column(db.INTEGER, default=1)


class Cart(db.Model):

    __tablename__ = 'axf_cart'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    c_user = db.Column(db.INTEGER, db.ForeignKey(AXFUser.id))
    c_goods = db.Column(db.INTEGER, db.ForeignKey(Goods.id))

    c_goods_num = db.Column(db.INTEGER, default=1)
    c_is_select = db.Column(db.Boolean, default=True)

