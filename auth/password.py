import hashlib
import secrets
import hmac

class Password:

    @staticmethod
    def hash_password(password):
        pass_hex = secrets.token_hex(16)

        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            pass_hex.encode(),
            600000
        ).hex()

        return f"{pass_hex} ${hashed}"
    

    @staticmethod
    def verify_pass(password, stored_pass):
        pass_hex, original_pass = stored_pass.split("$")

        new_pass = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            pass_hex.encode(),
            600000
        ).hex()

        return hmac.compare_digest(original_pass, new_pass)