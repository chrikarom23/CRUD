import sqlite3
from flask_jwt import JWT, jwt_required
from flask_restful import Resource, reqparse

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank")

    @classmethod
    def find_item(cls,name):
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        res = cur.execute("SELECT * FROM Items WHERE name = ?", (name,))
        conn.close()
        if res:
            return {'item': {'name': res[0], 'price': res[1]}}, 200

    @jwt_required()
    def get(self, name):
        result = Item.find_item(name)
        if result:
            print(result)
        return {'message': 'item not found'}, 404

    def post(self, name):
        #if next(filter(lambda x: x['name'] == name, items), None):
            #return {'message':f'An item with the name ({name})already exists'}
        result = Item.find_item(name)
        if result is not None:
            return {f"message":"An item with the name ({name}) already exists"}
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO Items VALUES (?,?)", (name, data['price']))
        conn.commit()
        conn.close()

        return item, 201

    def delete(self, name):
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM Items WHERE name = ?", (name,))
        conn.commit()
        conn.close()
        return {"message": "item deleted"}

    def put(self,name):
        result = Item.find_item(name)
        data = Item.parser.parse_args()

        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        if result:
            cur.execute("UPDATE Items SET price = ? WHERE name = ?", (data["price"], name))
        cur.execute("INSERT INTO Items VALUES ?,?", (name ,data["price"]))
        item = {'name': name, 'price': data['price']}
        conn.commit()
        conn.close()

        return item, 201


class Itemss(Resource):
    @jwt_required()
    def get(self):
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        res = cur.execute("SELECT * FROM Items")
        i = []
        for row in res:
            i.append({'name':row[0], 'price':row[1]})
        conn.close()
        return {'Items': i}
