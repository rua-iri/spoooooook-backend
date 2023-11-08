import json
import helpers
import constants

def lambda_handler(event, context):

    loginData = json.loads(event["body"])

    responseStatusCode = constants.ERROR_RESPONSE_CODE
    responseBody = {}
    

    if helpers.createUser(loginData):
        responseStatusCode = constants.SUCCESS_RESPONSE_CODE
        responseBody['message'] = "Registration Successful"
    else:
        responseBody['error'] = "Invalid Registration"


    return {
        "statusCode": str(responseStatusCode),
        "body": json.dumps(responseBody)
    }
