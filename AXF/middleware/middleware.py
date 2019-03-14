from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from App.models import AXFUser

REQUIRE_LOGIN_JSON = [
    '/axf/addtocart/',
    '/axf/changecartstate/',
    '/axf/makeorder/',
    '/axf/chooseaddress/',
    '/axf/addaddress/'
]

REQUIRE_LOGIN = [
    '/axf/cart/',
    '/axf/mine/',
    '/axf/orderlistnotpay/',
    '/axf/orderlistnotreceive/',
]


class LoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path in REQUIRE_LOGIN_JSON:
            user_id = request.session.get('user_id')
            if user_id:
                try:
                    user = AXFUser.objects.get(pk=user_id)
                    request.user = user
                except Exception:
                    data = {
                        'status': 302,
                        'msg': 'user not avaliable'
                    }
                    return JsonResponse(data=data)

        if request.path in REQUIRE_LOGIN:
            user_id = request.session.get('user_id')
            if user_id:
                try:
                    user = AXFUser.objects.get(pk=user_id)
                    request.user = user
                except:
                    return redirect(reverse('axf:login'))

            else:
                return redirect(reverse('axf:login'))
