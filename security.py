from user import User as u


def authenticate(username, password):
    user = u.find_user_by_name(username) # User(id, name, pass)
    if user and password == user.password:
        return user


def identity(payload):
    user_id = payload['identity']
    print("payload")
    return u.find_user_by_id(user_id)
