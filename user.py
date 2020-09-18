import sqlite3
from flask_restful import Resource, reqparse


class User():
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    def __str__(self):
        return f"ID:{self.id}, Username:{self.username}, Password:{self.password}"

    @classmethod
    def find_user_by_name(cls, username):
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users WHERE name=?",(username,))
        temp = cur.fetchone()
        if temp:
            tempv = cls(*temp)
        else:
            tempv = None
        conn.close()
        return tempv

    @classmethod
    def find_user_by_id(cls, _id):
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users WHERE id=?", (_id,))
        temp = cur.fetchone()
        if temp:
            tempv = cls(*temp)
        else:
            tempv = None
        conn.close()
        return tempv


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        help="This field cannot be left blank",
                        required=True)

    parser.add_argument("password",
                        help="This field cannot be left blank",
                        required=True)

    def post(self):
        data=UserRegister.parser.parse_args()

        if User.find_user_by_name(data["username"]):
            return {"message":"User with username already exists"}

        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO Users VALUES (NULL,?,?)", (data['username'], data['password']))

        conn.commit()
        conn.close()

        return {"message": "new user has been created"}
