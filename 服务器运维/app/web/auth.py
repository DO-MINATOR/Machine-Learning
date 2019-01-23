from app.web import web
from flask import render_template, request, redirect, url_for, flash
from app.form.authform import RegisterForm, LoginForm
from app.db.user import User
from app.db import db
from app.db.user import User
from flask_login import login_user,current_user


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        user.set_attrs(form.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('web.login'))
    else:
        return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash("用户名不存在或者密码错误")
    return render_template('auth/login.html',form=form)


@web.route('/reset/password')
def forget_password_request():
    pass


@web.route('/reset/password/<token>')
def forget_password(token):
    pass
