import hmac
import hashlib
import base64

from django.conf import settings
from rest_framework.exceptions import NotAuthenticated

from stargate_utils.aws import CLIENT

def get_secret_hash(username):
    msg = username + settings.CLIENT_ID
    dig = hmac.new(str(settings.CLIENT_SECRET).encode('utf-8'),
        msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def get_user_token(username, password):
    username = username.lower()
    username = username.strip()
    try:
        resp = CLIENT.admin_initiate_auth(
            UserPoolId=settings.USER_POOL_ID,
            ClientId=settings.CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'SECRET_HASH': get_secret_hash(username),
                'PASSWORD': password
            },
            ClientMetadata={
                'username': username,
                'password': password
            })
    except CLIENT.exceptions.NotAuthorizedException:
        raise NotAuthenticated("The username or password is incorrect.")

    except CLIENT.exceptions.UserNotConfirmedException:
        raise NotAuthenticated("User is not confirmed.")

    except Exception as e:
        raise NotAuthenticated(str(e))

    if 'AuthenticationResult' in resp:
        resp = {
            'access': resp['AuthenticationResult']['IdToken'],
            'refresh': resp['AuthenticationResult']['RefreshToken'],
            'token': resp['AuthenticationResult']['AccessToken']
        }

    return resp


def get_user_token_using_refresh_token(username, refresh_token):
    try:
        resp = CLIENT.admin_initiate_auth(
            UserPoolId=settings.USER_POOL_ID,
            ClientId=settings.CLIENT_ID,
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters={
                'REFRESH_TOKEN': refresh_token,
                'SECRET_HASH': get_secret_hash(username)
            }
        )
    except CLIENT.exceptions.NotAuthorizedException:
        return False, "Incorrect username or password"
    except CLIENT.exceptions.UserNotFoundException:
        return False, "Username does not exists"
    except Exception as e:
        return False, str(e)
    if 'AuthenticationResult' in resp:
        token = {
            'access': resp['AuthenticationResult']['IdToken'],
            'token': resp['AuthenticationResult']['AccessToken'],
            'refresh': refresh_token
        }
        return True, token
    return True, resp
