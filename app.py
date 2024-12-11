from flask import Flask, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from config import User
from flask_login import LoginManager, current_user, login_user, logout_user


app = Flask(__name__)


app = Flask(__name__)
app.secret_key = "secret"

# ログインマネージャーをインスタンス化
# ユーザーのログイン状態を管理してくれる便利なやつ
# login_managerのインスタンス化と初期化
login_manager = LoginManager()
login_manager.init_app(app)


# ログイン中のユーザー情報を取得するためのメソッド
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        if not request.form["name"] or not request.form["password"] or not request.form["email"]:
            flash("未入力の項目があります。")
            return redirect(request.url)
        if User.select().where(User.name == request.form["name"]):
            flash("その名前は既に使われています")
            return redirect(request.url)
        if User.select().where(User.email == request.form["email"]):
            flash("そのメールアドレスは既に使われています。")
            return redirect(request.url)

        User.create(
            name=request.form["name"],
            email=request.form["email"],
            password=generate_password_hash(request.form["password"]),
        )
        return render_template("index.html")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if not request.form["password"] or not request.form["email"]:
            flash("未入力の項目があります。")
            return redirect(request.url)

        user = User.select().where(User.email == request.form["email"]).first()
        if user is not None and check_password_hash(user.password, request.form["password"]):
            login_user(user)

            flash(f"ようこそ{user.name}さん")
            return redirect("/")
        flash("認証に失敗しました。")

    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    flash("ログアウトしました")
    return redirect("/")


@app.route("/unregister")
def unregister():
    current_user.delete_instance()
    logout_user()
    return redirect("/")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
