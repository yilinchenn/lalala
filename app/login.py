from flask import render_template, url_for, request, make_response, flash, redirect
from app import webapp
from app.models import User

@webapp.route('/login', methods=["GET", "POST"])
def login():
    if(request.method == 'POST'):
        return do_login(request.form)
    else:
        return render_template("login_form.html")


def do_login(form):
    if(form):
        username = form.get("username")
        password = form.get("password")

        usr = User.query.filter_by(username=username).first()
        if(usr):
            if(usr.check_password(password)):
                flash("INFO: log in successful")
                return redirect(url_for("dashboard"))
            else:
                flash("ERROR: wrong password")
                return redirect(url_for("login"))
        else:
            flash("ERROR: user does not exist")
            return redirect(url_for("login"))


    return make_response("not implemented")




