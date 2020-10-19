from flask import Flask, request, jsonify, render_template, redirect, session
import uuid
import os
from server.models import User, News

app = Flask(__name__)
app.config["SECRET_KEY"] = str(uuid.uuid4())


@app.route('/secret', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    username = request.form.get("username")
    password = request.form.get("password")
    with User() as users:
        user = users.find_user(username, password)
    if user and users.is_admin(username):
        session["current_user"] = user[0]
        session.modified = True
        return redirect("/admin")
    elif user:
        session["current_user"] = user[0]
        session.modified = True
        return redirect("/news")
    else:
        return redirect("/")
