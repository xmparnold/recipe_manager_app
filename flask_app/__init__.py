from flask import Flask

app = Flask(__name__)
app.secret_key = 'secret'
DATABASE = 'recipe_manager_schema'