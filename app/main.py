
from flask import render_template, url_for
from app import webapp


@webapp.route('/')
def main():
    return render_template("main.html")

@webapp.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

