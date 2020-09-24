import hmac
import hashlib
import base64
import logging

from django.conf import settings
from rest_framework.exceptions import APIException
import rest_framework.status as status
from stargate_utils.aws import CLIENT

log = logging.getLogger(__name__)


def get_secret_hash(username):
    msg = username + settings.CLIENT_ID
    dig = hmac.new(str(settings.CLIENT_SECRET).encode('utf-8'),
                   msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def add_user(username, attributes):
    username = username.lower()
    username = username.strip()
    try:
        new_user = CLIENT.admin_create_user(
                Username=username,
                UserPoolId=settings.USER_POOL_ID,
                UserAttributes=attributes,
                DesiredDeliveryMediums=["EMAIL"]
            )

    except CLIENT.exceptions.UsernameExistsException as e:
        log.error("Email already exists %s" % str(e))
        raise APIException("Email already exists", status.HTTP_409_CONFLICT)
    except Exception as e:
        log.error("Error while user registeration %s" % str(e))
        raise APIException("Error: {}".format(str(e)),
                           status.HTTP_400_BAD_REQUEST)
    
    user_details = new_user['User']
    return user_details


def check_if_group_exists(group_name_stripped):
    try:
        group = CLIENT.get_group(
            GroupName=group_name_stripped,
            UserPoolId=settings.USER_POOL_ID
        )
    except CLIENT.exceptions.ResourceNotFoundException as e:
        log.error("Group doesnt exists %s" % str(e))
        group = create_group(group_name_stripped)
    except Exception as e:
        log.error("Error while checking from group %s" % str(e))
        raise APIException.ParseError(
            "Exception in check_if_group_exists {}".format(str(e)),
            status.HTTP_400_BAD_REQUEST)
    return group


def create_group(group_name):
    try:
        resp = CLIENT.create_group(
            GroupName=group_name,
            UserPoolId=settings.USER_POOL_ID
        )
    except Exception as e:
        raise APIException.ParseError(
            "Exception in create_group {}".format(str(e)),
            status.HTTP_400_BAD_REQUEST)
    return resp


def add_user_to_group(user_details, group_name):
    try:
        response = CLIENT.admin_add_user_to_group(
            UserPoolId=settings.USER_POOL_ID,
            Username=user_details['Username'],
            GroupName=group_name
        )
    except Exception as e:
        log.error("Exception in add_user_to_group {}".format(str(e)))
        raise APIException.ParseError(
             "Exception in add_user_to_group {}".format(str(e)),
            status.HTTP_400_BAD_REQUEST)
    return response


def remove_user_from_group(user_details, group_name):
    try:
        response = CLIENT.admin_remove_user_from_group(
            UserPoolId=settings.USER_POOL_ID,
            Username=user_details['Username'],
            GroupName=group_name
        )
    except Exception as e:
        return False, "Exception in remove_user_from_group {}".format(str(e))
    return True, response
