import datetime
from app.model.admin import Admin
from app import response, app, db
from flask import flash, make_response, redirect, render_template, request, url_for
from flask_jwt_extended import create_access_token, create_refresh_token, unset_jwt_cookies, set_access_cookies

def index():
    return render_template('login.html')

def addAdmin():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        admins = Admin(name=name, email=email)
        admins.setPassword(password)
        db.session.add(admins)
        db.session.commit()

        return response.success('', 'Admin added successfully')
    except Exception as e:
        print(e)
        return response.success(str(e), 'gagal Admin added successfully')

def singleObject(data):
    data = {
        'id' : data.id,
        'name' : data.name,
        'email' : data.email
    }

    return data

def store():
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        admin = Admin.query.filter_by(email=email).first()

        if not admin:
            flash('Email tidak terdaftar', 'error')
            return redirect('/login')
        
        if not admin.checkPassword(password):
            flash('Password salah', 'error')
            return redirect('/login')
        
        # data = singleObject(admin)
        
        # expires = datetime.timedelta(days=7)
        # expires_refresh = datetime.timedelta(days=7)

        # access_token = create_access_token(identity=data, fresh=True, expires_delta=expires)
        # refresh_token = create_refresh_token(data, expires_delta=expires_refresh)

        response_login = redirect('/data-ulasan')
        access_token = create_access_token(identity=email)
        set_access_cookies(response_login, access_token)
        return response_login
    except Exception as e:
        print(e)
        flash('Gagal login: ' + str(e), 'error')
        return redirect('/login')

def logout():
    try:
        response = redirect(url_for("login"))
        unset_jwt_cookies(response)
        return response
    except Exception as e:
        print(e)
        return response.success(str(e), 'Failed to logout')