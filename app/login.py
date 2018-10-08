from flask import render_template, url_for, request, make_response, flash, redirect, session
from app import webapp
from app.models import User

@webapp.route('/login', methods=["GET", "POST"])
def login():
    if(request.method == 'POST'):
        return do_login(request.form)
    else:
        return render_template("login_form.html")

@webapp.route('/logout', methods=["POST"])
def logout():
    return do_logout(request.form)

def do_login(form):
    if(form):
        username = form.get("username")
        password = form.get("password")

        usr = User.query.filter_by(username=username).first()
        if(usr):
            if(usr.check_password(password)):
                #set session
                session['username'] = username
                return redirect(url_for("dashboard", username=username))
            else:
                flash("ERROR: wrong password")
                return redirect(url_for("login"))
        else:
            flash("ERROR: user does not exist")
            return redirect(url_for("login"))

def do_logout(form):
    if(check_session(form.get("username"))):
        session.pop('username', None)
        flash("INFO: logout successful")
        return redirect(url_for('login'))

def check_session(username):
    if(session.get('username')):
        if username == session['username']:
            return True
    return False
