import os
from stargate_utils.aws import CLIENT

USER_POOL_ID = os.environ["AWS_COGNITO_USER_POOL_ID"]
CLIENT_ID = os.environ["AWS_COGNITO_CLIENT_ID"]
CLIENT_SECRET = os.environ["AWS_COGNITO_CLIENT_SECRET"]

def add_new_test_student(username, firstname, lastname, password):
    payload = {"first_name": firstname ,
               "last_name": lastname ,
               "email": username ,
               "agree": True ,
               "instance": "" ,
               "institute_logo": ""
               }
    print(payload)
    headers = {}
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "application/json"
    newuser = requests.post("https://gps-v2.goeducate.com/pt/api/v2/signup" , 
                            json=payload,headers=headers
                            )
    # print(newuser.text)
    print(newuser.status_code)




    response = CLIENT.admin_set_user_password(
        UserPoolId=USER_POOL_ID,
        Username=username,
        Password=password,
        Permanent=True
    )
