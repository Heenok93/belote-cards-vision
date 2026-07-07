from streamlit_authenticator.utilities.hasher import Hasher

passwords = ["admin", "test123"]

hashed_passwords = Hasher.hash_list(passwords)

for hashed in hashed_passwords:
    print(hashed)