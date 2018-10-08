from flask import render_template, url_for, request, make_response
from app import webapp


@webapp.route('/login', methods=["GET", "POST"])
def login():
    if(request.method == 'POST'):
        return do_login()
    else:
        return render_template("login_form.html")


def do_login():
    return make_response("not implemented")




