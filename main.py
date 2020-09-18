from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from Items import Item, Itemss
from db import dbcheck
from security import authenticate, identity
from user import UserRegister

dbcheck()
app = Flask(__name__)
app.secret_key = 'ckr'
api = Api(app)

jwt = JWT(app, authenticate, identity)


api.add_resource(Item, '/items/<string:name>')
api.add_resource(Itemss, '/items')
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True)
