import bcrypt


class PasswordChecker:
    def __init__(self):
        pass

    def validate_password(self, password):
        if len(password) < 8:
            return False

        if not any(char.isupper() for char in password):
            return False

        if not any(char.islower() for char in password):
            return False

        if not any(char.isdigit() for char in password):
            return False

        symbols = "!@#$%^&*()-_=+[]{}|;:',.<>?`~"
        if not any(char in symbols for char in password):
            return False

        return True


    def check_pass_against_db_pass(self, user_input_pass, hashed_pass):
        user_input_pass_bytes = user_input_pass.encode('utf-8')
        hashed_pass_bytes = hashed_pass.encode('utf-8')
        if bcrypt.checkpw(user_input_pass_bytes, hashed_pass_bytes):
            return True
        else:
            return False


    def generate_password_hash(self, password):
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_pass = bcrypt.hashpw(password_bytes, salt)
        return hashed_pass
