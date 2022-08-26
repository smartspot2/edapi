from edapi import EdAPI

ed = EdAPI()
ed.login()

user_info = ed.get_user_info()
user = user_info["user"]

print(f"Hello {user['name']}!")
