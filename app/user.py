from flask import render_template, url_for, request, make_response
from app import webapp


@webapp.route('/user/<user_id>', methods=["GET", "POST"])
def existing_user(user_id):
    #TODO: auth
    if(request.method == 'POST'):
        return do_update_user()
    else:
        return "display user form"


@webapp.route('/user/new', methods=["GET", "POST"])
def new_user():
    if(request.method == 'POST'):
        return do_create_user()
    else:
        return render_template("user_form.html")


def do_update_user():
     return ("not implemented")


def do_create_user():
    #return make_response("not implemented")
    return "not implemented"