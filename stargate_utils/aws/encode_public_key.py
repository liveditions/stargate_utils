import json, base64, sys

def get_encoded_public_key(jwks):
    # https://cognito-idp.us-east-1.amazonaws.com/<Pool_id>/.well-known/jwks.json
    return base64.urlsafe_b64encode(json.dumps(jwks).encode()).decode()
