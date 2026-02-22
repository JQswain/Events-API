from models import User

def test_user_hashing_password_behaves_as_expected():
    user = User()
    user.set_password("chicken")
    assert user.password_hash != "chicken"

def test_check_user_password():
    user = User()
    user.set_password("password123")
    assert user.check_password("password123")
