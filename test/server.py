from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId

app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(
        host='localhost',
        port=27017,
        serverSelectionTimeoutMS=1000
    )
    db = mongo.company
    mongo.server_info()  # если нельзя подключиться к бд
except:
    print("Ошибка - невозможно подключиться к базе данных")


@app.route("/")
def index():
    return "Hello World!"


@app.route("/users", methods=['GET'])
def get_some_users():
    try:
        data = list(db.users.find())
        for user in data:
            user['_id'] = str(user['_id'])
        return Response(
            response=json.dumps(data),
            status=500,
            mimetype='application/json'
        )
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "cannot read users"}), status=500, mimetype='application/json')


# создание юзера
@app.route("/users", methods=['POST'])
def create_user():
    try:
        user = {
            "name": request.form["name"],
            "lastname": request.form["lastname"]
        }
        dbResponse = db.users.insert_one(user)
        print(dbResponse.inserted_id)
        # for attr in dir(dbResponse):
        #     print(attr)
        return Response(
            response=json.dumps(
                {"message": "user created",
                 "id": f"{dbResponse.inserted_id}"
                 }),
            status=200,
            mimetype='application/json'
        )
    except Exception as ex:
        print('******')
        print(ex)
        print('******')


# редактирование юзера
@app.route("/users/<id>", methods=["PATCH"])
def update_user(id):
    try:
        db.Response = db.users.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"name": request.form["name"], "lastname": request.form["lastname"]}}
        )
        # for attr in dir(db.Response):
        #     print(f'*****{attr})*****')
        if db.Response.modified_count == 1:
            return Response(
                response=json.dumps({"message": "user updated"}),
                status=200,
                mimetype='application/json')
        return Response(
            response=json.dumps({"message": "nothing to update"}),
            status=200,
            mimetype='application/json'
        )
    except Exception as ex:
        print('**********')
        print(ex)
        print('**********')
        return Response(
            response=json.dumps({"message": "cannot update user", }),
            status=500,
            mimetype='application/json'
        )


# удаление юзера
@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        db.Response = db.users.delete_one({"_id": ObjectId(id)})
        if db.Response.deleted_count == 1:
            return Response(response=json.dumps({"message": "user deleted", "id": f"{id}"}), status=200,
                            mimetype='application/json')
        return Response(response=json.dumps({"message": "user not found", "id": f"{id}"}), status=200,
                        mimetype='application/json')

    except Exception as ex:
        print('**********')
        print(ex)
        print('**********')
        return Response(
            response=json.dumps({"message": "cannot delete user", }),
            status=500,
            mimetype='application/json'
        )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4567, debug=True)
