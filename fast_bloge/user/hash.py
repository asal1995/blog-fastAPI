from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes='bcrypt', deprecated='auto')


class Hash:

    @staticmethod
    def bcrypt(password):
        return pwd_ctx.hash(password)

    @staticmethod
    def verify(hash_password, plain_password):
        pwd_ctx.verify(plain_password, hash_password)
