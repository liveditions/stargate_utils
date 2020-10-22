import os
from stargate_utils.aws import CLIENT

USER_POOL_ID = os.environ["AWS_COGNITO_USER_POOL_ID"]
CLIENT_ID = os.environ["AWS_COGNITO_CLIENT_ID"]
CLIENT_SECRET = os.environ["AWS_COGNITO_CLIENT_SECRET"]

def add_new_test_student(username, firstname, lastname, password):
    attributes = [
        {
            "Name": "email_verified",
            "Value": "true"
        },
        {
            "Name": "custom:student_type",
            "Value":  ''
        },
        {
            "Name": "custom:UserType",
            "Value": "Student"
        },
        {
            "Name": "custom:user_portal",
            "Value": "GPS"
        },
        {
            "Name": "custom:college_name",
            "Value": str([])
        },
        {
            "Name": "custom:institution_uuid",
            "Value": str([])
        },
        {
            "Name": "given_name",
            "Value": firstname
        },
        {
            "Name": "family_name",
            "Value": lastname
        },
        {
            "Name": "email",
            "Value": username
        },
        {
            "Name": "custom:logo",
            "Value":  ''
        }
    ]


    new_user = CLIENT.admin_create_user(
        Username=username,
        UserPoolId=USER_POOL_ID,
        UserAttributes=attributes,
        MessageAction="SUPPRESS"
    )

    response = CLIENT.admin_set_user_password(
        UserPoolId=USER_POOL_ID,
        Username=username,
        Password=password,
        Permanent=True
    )
