import os
from flask import Flask, redirect, render_template, jsonify, request, flash, url_for
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from sqlalchemy.exc import OperationalError, IntegrityError
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

from App.models import User, Routine, Exercise

from App.database import init_db, db
from App.config import load_config

from App.controllers import (
    setup_jwt,
    add_auth_context
)

from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
    current_user,
    set_access_cookies,
    unset_jwt_cookies,
    current_user,
)

from App.views import views

def add_views(app):
    for view in views:
        app.register_blueprint(view)

def create_app(overrides={}):
    app = Flask(__name__, static_url_path='/static')
    load_config(app, overrides)
    CORS(app)
    add_auth_context(app)
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app)
    init_db(app)
    jwt = setup_jwt(app)
    
    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return render_template('401.html', error=error), 401
    
    app.app_context().push()
    return app

app = create_app()
db.init_app(app)

jwt = JWTManager(app)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user

@jwt.user_identity_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.get(identity)

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    flash("Your session has expired. Please log in again.")
    return redirect(url_for('login'))

def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = create_access_token(identity=username)
        response = jsonify(access_token=token)
        set_access_cookies(response, token)
        return response
    return jsonify(error="Invalid username of password"), 401

@app.route('/')
def index():
    return render_template('layout.html')

@app.route('/login', methods=['POST'])
def login_action():
  username = request.form.get('username')
  password = request.form.get('password')
  user = User.query.filter_by(username=username).first()
  if user and user.check_password(password):
    response = redirect(url_for('layout.html'))
    access_token = create_access_token(identity=user.id)
    set_access_cookies(response, access_token)
    return response
  else:
    flash('Invalid username or password')
    return redirect(url_for('login.html'))
  
def create_users():
    rob = User(username="rob", password="robpass")
    bob = User(username="bob", password="bobpass")
    db.session.add_all([rob, bob])
    db.session.commit()
