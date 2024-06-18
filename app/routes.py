from flask import jsonify, redirect, request, render_template
from app import app, response
from app.controller import UlasanController, AdminController
from flask_jwt_extended import unset_jwt_cookies, get_jwt_identity, jwt_required

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

@app.route('/add-admin', methods=['POST'])
def admins():
    if request.method == 'POST':
        # return 'test'
        return AdminController.addAdmin()
    else:
        return 'method not allowed'

@app.route('/data-ulasan', methods=['GET', 'POST'])
@jwt_required()
def dataUlasan():
    if request.method == 'GET':
        return UlasanController.index()
    elif request.method == 'POST':
        return UlasanController.index()
    else:
        return jsonify({'error': 'Method not allowed'}), 405

@app.route('/logout', methods=['GET'])
def logout():
    try:
        unset_jwt_cookies(response=redirect('/login'))
        
        return redirect('/login')
    except Exception as e:
        print(e)
        return response.success(str(e), 'Failed to logout')


