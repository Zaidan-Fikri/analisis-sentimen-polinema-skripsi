from flask import jsonify, redirect, request, render_template
from app import app, response
from app.controller import UlasanController, AdminController
from flask_jwt_extended import unset_jwt_cookies, get_jwt_identity, jwt_required

# csrf = CSRFProtect(app)

@app.route('/')
def inputUlasan():
    return render_template('input-ulasan.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return AdminController.index()
    elif request.method == 'POST':
        return AdminController.store()
    else:
        return 'Method not allowed'

# csrf.exempt(login)

@app.route('/ulasan', methods=['POST'])
def ulasans():
    if request.method == 'POST':
        return UlasanController.predict()
    else:
        return 'method not allowed'

# csrf.exempt(ulasans)

@app.route('/add-admin', methods=['POST'])
def admins():
    if request.method == 'POST':
        # return 'test'
        return AdminController.addAdmin()
    else:
        return 'method not allowed'

# csrf.exempt(admins)

@app.route('/data-ulasan', methods=['GET'])
@jwt_required()
def dataUlasan():
    if request.method == 'GET':
        return UlasanController.index()
    else:
        return jsonify({'error': 'Method not allowed'}), 405


# @app.route('/data-ulasan-filter', methods=['GET'])
# @jwt_required()
# def dataUlasanFilter():
#     if request.method == 'GET':
#         return UlasanController.index()
#     else:
#         return jsonify({'error': 'Method not allowed'}), 405  

# csrf.exempt(dataUlasan)

@app.route('/logout', methods=['GET'])
def logout():
    try:
        return AdminController.logout()
    except Exception as e:
        print(e)
        return response.success(str(e), 'Failed to logout')


