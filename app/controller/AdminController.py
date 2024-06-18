import datetime
from app.model.admin import Admin
from app import response, app, db
from flask import redirect, render_template, request
from flask_jwt_extended import create_access_token, create_refresh_token, unset_jwt_cookies

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
            return response.badRequest([], 'email tidak terdaftar')
        
        if not admin.checkPassword(password):
            return response.badRequest([], 'password salah')
        
        data = singleObject(admin)
        
        expires = datetime.timedelta(days=7)
        expires_refresh = datetime.timedelta(days=7)

        access_token = create_access_token(data, fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(data, expires_delta=expires_refresh)

        return redirect('/data-ulasan')
        # return response.success({
        #     "data" : data,
        #     "access_token" : access_token,
        #     "refresh_token" : refresh_token
        # }, "success login")
    except Exception as e:
        print(e)
        return response.success(str(e), 'gagal login')

def logout():
    try:
        # Unset JWT cookies to logout the user
        unset_jwt_cookies(response=redirect('/login'))
        
        return redirect('/login')
    except Exception as e:
        print(e)
        return response.success(str(e), 'Failed to logout')