from src.core.utils.hash import PasswordHashed

p = PasswordHashed()

password = "123456789"

result = p.hash_password(password)
print(result)
