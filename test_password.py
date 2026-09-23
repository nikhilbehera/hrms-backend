from password import hash_password,verify_password

password = "hello12563"

hashed = hash_password(password)
print("Hashed:",hashed)
print("correct password:", verify_password("mypassword", hashed))
print("wrong password:", verify_password("wrongpassword", hashed))