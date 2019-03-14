from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^home/', views.home, name='home'),

    url(r'^market/', views.market, name='market'),

    url(r'^marketwithparams/(?P<typeid>\d+)/(?P<childid>\d+)/(?P<order_rule>\d+)/', views.market_with_params, name='market_with_params'),

    url(r'^cart/', views.cart, name='cart'),

    url(r'^mine/', views.mine, name='mine'),

    url(r'^register/', views.register, name='register'),

    url(r'^activate/', views.activate, name='activate'),

    url(r'^login/', views.login, name='login'),

    url(r'^logout/', views.logout, name='logout'),

    url(r'filemodify/', views.file_modify, name='file_modify'),

    url(r'^checkuser/', views.check_user, name='check_user'),

    url(r'^addtocart/', views.add_to_cart, name='add_to_cart'),

    url(r'^subshopping/', views.sub_shopping, name='sub_shopping'),

    url(r'^addshopping/', views.add_shopping, name='add_shopping'),

    url(r'^changecartstate/', views.change_cart_state, name='change_cart_state'),

    url(r'^allselect/', views.all_select, name='all_select'),

    url(r'^makeorder/', views.make_order, name='make_order'),

    url(r'^orderdetail/', views.order_detail, name="order_detail"),

    url(r'^orderlistnotpay/', views.order_list_not_pay, name='order_list_not_pay'),

    url(r'^orderlistnotreceive/', views.order_list_not_receive, name='order_list_not_receive'),

    url(r'^alipay/', views.alipay, name='alipay'),

    url(r'^payed/', views.payed, name='payed'),

    url(r'^chooseaddress/', views.choose_address, name='choose_address'),

    url(r'^addaddress/', views.add_address, name='add_address'),

    url(r'^addresslist', views.address_list, name='address_list')


]