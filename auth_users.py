from get_tasks import authenticate_user

users = [
    "1@gmail.com",
    "2@gmail.com"
]

for user in users:
    print("Authenticating ", user)
    creds = authenticate_user(user)