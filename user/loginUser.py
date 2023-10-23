import json

def lambda_handler(event, context):

    loginData = json.loads(event["body"])

    # rspnse = userLogin(
    #     loginData["username"],
    #     loginData["password"],
    # )


    return {
        "statusCode": 200,
        "body": json.dumps(loginData)
    }
