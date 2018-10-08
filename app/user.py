from flask import render_template, url_for, request, redirect
from app import webapp
from app.models import User
from app import db


@webapp.route('/user/<user_id>', methods=["GET", "POST"])
def existing_user(user_id):
    #TODO: auth
    if(request.method == 'POST'):
        return do_update_user(request.form)
    else:
        return "display user form"


@webapp.route('/user/new', methods=["GET", "POST"])
def new_user():
    if(request.method == 'POST'):
        return do_create_user(request.form)
    else:
        return render_template("user_form.html")


def do_update_user(form):
     return ("not implemented")


def do_create_user(form):
    if(form):
        print(form)
        usr = User(username=form.get("username"),
                   password=form.get("password"),
                   is_admin=False)
        print(usr)
        db.session.add(usr)
        db.session.commit()
        return redirect(url_for('dashboard'))

