from flask import session, request, render_template, redirect, flash
from flask_app import app
from flask_app.models.recipe_model import Recipe
from flask_app.models.user_model import User

@app.route( "/display/recipe" )
def display_recipe():
    if User.validate_session():
        return render_template( "recipeForm.html" )
    else:
        return redirect( "/" )

@app.route( "/dashboard" )
def display_dashboard():
    if User.validate_session():
        recipes = Recipe.get_all()
        return render_template( "dashboard.html", recipes = recipes )
    else:
        return redirect( "/" )

@app.route( "/recipe/new", methods = [ 'POST' ] )
def create_recipe():
    # TODO: Validate that fields are not empty
    data = {
        "name" : request.form[ 'name' ],
        "description" : request.form[ 'description' ],
        "instructions" : request.form[ 'instructions' ],
        "user_id" : session[ 'user_id' ]
    }

    Recipe.create( data )
    return redirect( "/dashboard" )

@app.route( "/recipe/<int:id>" )
def get_recipe( id ):
    if User.validate_session():
        data = {
            "id" : id
        }

        recipe = Recipe.get_one( data )

        if recipe == None:
            # TODO: Flash error message
            pass
        else:
            return render_template( "displayRecipe.html", recipe = recipe )
    else:
        return redirect( "/" )

@app.route( "/recipe/delete/<int:id>" )
def delete_recipe( id ):
    data = {
        "id" : id
    }

    Recipe.delete_one( data )
    return redirect( "/dashboard" )

@app.route( "/recipe/edit/<int:id>" )
def display_edit_recipe( id ):
    if User.validate_session():
        data = {
            "id" : id
        }
        recipe = Recipe.get_one( data )
        return render_template( "editRecipe.html", recipe = recipe )
    else:
        return redirect( "/" )

@app.route( "/recipe/edit/<int:id>", methods = [ 'POST' ] )
def edit_recipe( id ):
    data = {
        "id" : id,
        "name" : request.form[ 'name' ],
        "description" : request.form[ 'description' ],
        "instructions" : request.form[ 'instructions' ],
        "user_id" : session[ 'user_id' ]
    }

    Recipe.edit_one( data )
    return redirect( "/dashboard" )