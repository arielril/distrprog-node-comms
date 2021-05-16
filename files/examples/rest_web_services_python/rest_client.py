import json, requests

if __name__ == '__main__':
	response = requests.get("http://localhost:5000/user/Mary")
	print(response.status_code)
	print(response.content)

	user_info = {"name": "Jane", "age": 44, "occupation": "Bus driver", "address": "Nowhere, 455"}
	response = requests.put("http://localhost:5000/user/Jane", data = user_info)
	print(response.status_code)

	response = requests.get("http://localhost:5000/user/Jane")
	print(response.status_code)
	print(response.content)
