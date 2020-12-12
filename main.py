import functools
import os

from flask import Flask, request, render_template, redirect
import users
import driveAPI as g
import encryption as e

app = Flask(__name__)

userLogedIn = False
userNick = ""


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not userLogedIn:
            return redirect("/login")

        return view(**kwargs)

    return wrapped_view


@app.route("/", methods=['GET'])
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    global userLogedIn
    if request.method == 'GET':
        if userLogedIn:
            return redirect("/")
        return render_template('login.html')
    elif request.method == 'POST':
        nick = request.form['username']
        pwd = request.form['password']
        if users.login(nick, pwd):
            userLogedIn = True

        return redirect("/")


@app.route("/register", methods=['GET', 'POST'])
def register():
    global userLogedIn
    if request.method == 'GET':
        if userLogedIn:
            return redirect("/")
        return render_template('register.html')
    elif request.method == 'POST':
        nick = request.form['username']
        pwd = request.form['password']
        if users.login(nick, pwd):
            userLogedIn = True

        return redirect("/")


@app.route("/generate", methods=['GET', 'POST'])
@login_required
def generate_key():
    if request.method == 'GET':
        e.keyGen()
        return redirect("/")


@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    files = os.listdir("Files")
    if request.method == 'GET':
        return render_template('upload.html', files=files)
    elif request.method == 'POST':
        file_name = request.form['filename']
        e.encrypt(file_name, e.keyRead())
        g.uploadFile(file_name)

        return redirect("/")


@app.route("/download", methods=['GET', 'POST'])
@login_required
def download():
    files = os.listdir("EncFiles")
    if request.method == 'GET':
        return render_template('download.html', files=files)  # ,files=g.listFiles())
    if request.method == 'POST':
        file_name = request.form['filename']
        fileID = g.fileID(file_name)
        g.downloadFile(fileID, file_name)
        e.decrypt(file_name, e.keyRead())
        return redirect("/")


@app.route("/logout", methods=['GET'])
@login_required
def logout():
    global userLogedIn
    userLogedIn = False
    return redirect("/")


if __name__ == '__main__':
    app.run()
