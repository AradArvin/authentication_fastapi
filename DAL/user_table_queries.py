from db.db_manager import UserData


def create_user_query(user_data):
    try:
        user = UserData.create(**user_data)
        return user
    except Exception as ex:
        print(ex)
        return None


def get_user_query(username= None, user_id=None):
    try:
        if user_id:
            return UserData.get(UserData.id==user_id)
        else:
            return UserData.get(UserData.username==username)
    except Exception as ex:
        print(ex)
        return None


def delete_user_query(username):
    user = get_user_query(username)
    if user:
        user.delete_instance()


def user_exists(username):
    try:
        check = UserData.select().where(UserData.username==username).exists()
        return check
    except Exception as ex:
        return False