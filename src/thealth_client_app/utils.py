from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()

#This function hashes the password that the employee enters so that
#the password is not stored in the database as plaintext, which is
#a huge security risk.
def hash_pass(pw: str):
    return pwd_context.hash(pw)

def verify_pass(plain_pass: str, hashed_pass: str):
    return pwd_context.verify(plain_pass, hashed_pass)
