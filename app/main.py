
from flask import render_template, url_for, session, redirect, request, flash
from app import webapp
from app.login import check_session
from app.photo import get_thumbs, get_transformations


@webapp.route('/')
def main():
    if session.get('username'):
        return redirect(url_for('dashboard', username=session.get('username')))
    return render_template("main.html")

@webapp.route('/dashboard/<username>')
def dashboard(username):

    if(check_session(username)):
        thumbs = get_thumbs(session.get('username'))
        return render_template('dashboard.html', thumbs=thumbs)
    else:
        flash("Error: you are not logged in")
        return redirect(url_for('login'))


