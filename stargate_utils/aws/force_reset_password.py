import hmac
import hashlib
import base64

from rest_framework.exceptions import NotAuthenticated
from django.conf import settings
from stargate_utils.aws import CLIENT


def get_secret_hash(username):
    msg = username + settings.CLIENT_ID
    dig = hmac.new(str(settings.CLIENT_SECRET).encode('utf-8'),
        msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def force_reset_password(username, new_password, session,
                         challengename='NEW_PASSWORD_REQUIRED'):
    username = username.lower()
    username = username.strip()
    try:
        res_change_password = CLIENT.admin_respond_to_auth_challenge(
            UserPoolId=settings.USER_POOL_ID,
            ClientId=settings.CLIENT_ID,
            ChallengeName=challengename,
            ChallengeResponses={
                'USERNAME':username,
                'NEW_PASSWORD':new_password,
                'SECRET_HASH':get_secret_hash(username)
            },
            Session=session   
        )
    except CLIENT.exceptions.NotAuthorizedException:
        raise NotAuthenticated('Invalid session for the user.')
    except CLIENT.exceptions.CodeMismatchException:
        raise NotAuthenticated('Invalid session for the user, code mismatch.')
    except Exception as e:
        raise NotAuthenticated(str(e))
    
    token = {
            'access': res_change_password['AuthenticationResult']['IdToken'],
            'refresh': res_change_password['AuthenticationResult']['RefreshToken'],
            'token': res_change_password['AuthenticationResult']['AccessToken']
        }
    
    return token