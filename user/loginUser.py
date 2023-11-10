import json
import helpers
import constants

def lambda_handler(event, context):

    loginData = json.loads(event["body"])

    responseStatusCode = constants.ERROR_RESPONSE_CODE
    responseBody = {}

    if helpers.checkUser(loginData):
        responseStatusCode = constants.SUCCESS_RESPONSE_CODE
        responseBody['message'] = "Login Successful"
        responseBody['auth_token'] = helpers.generateJWT(loginData['username'])
    else:
        responseBody['error'] = "Invalid Login"


    return {
        "statusCode": str(responseStatusCode),
        "body": json.dumps(responseBody)
    }
