from flask import jsonify, redirect, request, render_template, url_for
from app import app, response
from app.controller import UlasanController, AdminController
from flask_jwt_extended import jwt_required
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError

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

@app.route('/logout', methods=['GET'])
def logout():
    try:
        return AdminController.logout()
    except Exception as e:
        print(e)
        return response.success(str(e), 'Failed to logout')

@app.errorhandler(NoAuthorizationError)
@app.errorhandler(InvalidHeaderError)
def handle_auth_error(e):
    return redirect(url_for('login'))
