from auth import create_access_token, verify_access_token


token = create_access_token("nikhil")

print("TOKEN:")
print(token)

username = verify_access_token(token)

print("USERNAME:")
print(username)