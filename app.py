import os


from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db  # this is new

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgres://znjouwhlzhpxpf:95861fbb8371f07d922cb11a83939d1db707430fe4ebe0d167d57aea74843f7e@ec2-107-20-104-234.compute-1.amazonaws.com:5432/d3i04e0snghupc')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)


@app.before_first_request  # This will create tables before the first request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    #from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
