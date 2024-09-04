from jwt import decode

from fast_zero.security import create_access_token
from fast_zero.settings import Settings

settings = Settings()


def test_jwt():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data)

    result = decode(token, settings.SECRET_KEY, [settings.ALGORITHM])

    assert result['sub'] == data['sub']
    assert result['exp']
