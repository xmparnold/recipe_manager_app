from flask import session, request, render_template, redirect, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt( app )

@app.route( "/" )
def display_login_registration():
    if User.validate_session():
        return redirect( "/dashboard" )
    else:
        return render_template( "index.html" )

@app.route( "/user/new", methods = ['POST'] )
def create_user():

    # Validate form fields contain values
    if User.validate_register( request.form ) == True:
        data = {
            "email" : request.form[ 'email' ]
        }

        result = User.get_one( data )

        if result == None:
            # add the new user because this means they don't exist
            data = {
                "email" : request.form[ 'email' ],
                "first_name" : request.form[ 'first_name' ],
                "last_name" : request.form[ 'last_name' ],
                "password" : bcrypt.generate_password_hash( request.form[ 'password' ] )
            }
            user_id = User.create( data )
            session[ 'email' ] = request.form[ 'email' ]
            session[ 'first_name' ] = request.form[ 'first_name' ]
            session[ 'last_name' ] = request.form[ 'last_name' ]
            session[ 'user_id' ] = user_id
            return redirect( "/dashboard" )
        else:
            flash( "Email already exists, please use another.", "error_register_email" )
            return redirect( "/" )
    else:
        return redirect( "/" )

@app.route( "/logout" )
def logout():
    session.clear()
    return redirect( "/" )

@app.route( "/login", methods = [ 'POST' ] )
def login():
    data = {
        "email" : request.form[ 'email' ]
    }
    result = User.get_one( data )

    if result == None:
        flash( "Wrong credentials", "error_login")
        return redirect( "/" )
    else:
        if not bcrypt.check_password_hash( result.password, request.form[ 'password' ] ):
            flash( "Wrong credentials", "error_login" )
            return redirect( "/" )
        else:
            session[ 'email' ] = result.email
            session[ 'first_name' ] = result.first_name
            session[ 'last_name' ] = result.last_name
            session[ 'user_id' ] = result.id
            return redirect( "/dashboard" )