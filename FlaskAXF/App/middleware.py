from flask import request, url_for, session, render_template

from App.models import AXFUser


def init_middleware(app):

    url_list = ['/mine/']

    @app.before_request
    def before():
        if request.path in url_list:
            print("----------before_request_catched-----------", request.url)
            user_id = session.get("user_id")
            print("user_id: ", session.get("user_id"))
            if user_id:
                user = AXFUser.query.get(user_id)
                print(user.u_username)
                if user:
                    request.user = user
            else:
                return render_template('user/login.html')
        else:
            # print("----------not catch---------------------------")
            pass
    @app.after_request
    def after(resp):
        return resp
