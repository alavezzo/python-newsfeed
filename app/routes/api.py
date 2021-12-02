from flask import Blueprint, request, jsonify, session
from app.models import User 
from app.db import get_db
import sys 

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users', methods=['POST'])
def signup():
    data = request.get_json()
    db = get_db()
    
    try: 
        # attempt creating a new User
        newUser = User(
            username = data['username'],
            email = data['email'],
            password = data['password']
        )

        db.add(newUser)
        db.commit()
        # if db.commit() fails the connection will remain in a pending state (won't notice in a local development setting but will lock up a production setting)
       
    except: 
        # insert failed, so send error to front end
        print(sys.exc_info()[0])

        #insert failed, so rollback and send error to front end and make it so connection doesn't stay in a pending state
        db.rollback()
        return jsonify(message = 'Signup failed'), 500
        
    # after login need a way to keep track of a user's logged in status, in express you could register the express-session npm package as middleware which exposes a req.session property on every request. In flask sessions belongf to a global object similar to g and request
    # you can create sessions in Flask only if you've defined a secret key, code in app/_init_.py does that 

    session.clear()
    session['user_id'] = newUser.id
    session['loggedIn'] = True

    return jsonify(id = newUser.id)