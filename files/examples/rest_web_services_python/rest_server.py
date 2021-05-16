from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

users = [
	{
		"name": "John",
		"age": 32,
		"occupation": "Butcher",
		"address": "Hope Street, 1234, Somewhere"
	},
	{
		"name": "Mary",
		"age": 27,
		"occupation": "Engineer",
		"address": "Grass, 777, Elysian Fields"
	}
]

class User(Resource):
	def get(self, name):
		for user in users:
			if(name == user["name"]):
				return user, 200
		return "User not found", 404

	def post(self, name):
		parser = reqparse.RequestParser()
		parser.add_argument("age")
		parser.add_argument("occupation")
		parser.add_argument("address")
		args = parser.parse_args()

		for user in users:
			if (name == user["name"]):
				return "User with name {} already exists".format(name), 400

		user = {
			"name": name,
			"age": args["age"],
			"occupation": args["occupation"],
			"address": args["address"]
		}
		users.append(user)
		return user, 201

	def put(self, name):
		parser = reqparse.RequestParser()
		parser.add_argument("age")
		parser.add_argument("occupation")
		parser.add_argument("address")
		args = parser.parse_args()

		for user in users:
			if (name == user["name"]):
				user["age"] = args["age"]
				user["occupation"] = args["occupation"]
				user["address"] = args["address"]
				return user, 200
		user = {
			"name": name,
			"age": args["age"],
			"occupation": args["occupation"],
			"address": args["address"]
		}
		users.append(user)
		return user, 201

	def delete(self, name):
		i = 0
		for user in users:
			if (name == user["name"]):
				del(users[i])
				return "user deleted.", 200
			i = i + 1
		return "User not found", 404

api.add_resource(User, "/user/<string:name>")

app.run(host='0.0.0.0', debug=True)
