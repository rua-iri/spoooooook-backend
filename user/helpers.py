import os
import boto3
import bcrypt

dbClient = boto3.client("dynamodb")
USER_TABLE = os.environ.get("UsersTable");


def checkUser(userCred):
    userRecord = dbClient.get_item(TableName=USER_TABLE, Key={
        "username": {"S": userCred.username}
    })

    if "Item" in userRecord:
        bcrypt.checkpw(bytes(userCred['password'], "utf-8"), 
                       bytes(userRecord['Item']['password']['s'], "utf-8"))
    else:
        return False



def createUser(userData):
    salt = bcrypt.gensalt()
    encryptedPassword = bcrypt.hashpw(userData['password'], salt=salt)
    
    # try to add the new user, as long as username is unique
    try:
        dbClient.put_item(
            TableName=USER_TABLE, 
            Item={
                'username': {
                    'S': userData['username']
                },
                'password': {
                    'S': encryptedPassword.decode()
                }
            },
            ConditionExpression='attribute_not_exists(username)'
        )

        return True

    except:
        return False

