import os
import boto3
import bcrypt
import time
import jwt
import dotenv

dbClient = boto3.client("dynamodb")
USER_TABLE = os.environ.get("DB_NAME");
dotenv.load_dotenv()
JWT_SECRET = os.getenv('JWT_SECRET')


def checkUser(userCred):
    userRecord = dbClient.get_item(TableName=USER_TABLE, Key={
        "username": {"S": userCred['username']}
    })

    if "Item" in userRecord:
        return bcrypt.checkpw(bytes(userCred['password'], "utf-8"), 
                       bytes(userRecord['Item']['password']['S'], "utf-8"))
    else:
        return False



def createUser(userData):
    st=time.perf_counter()
    salt = bcrypt.gensalt(rounds=6)
    encryptedPassword = bcrypt.hashpw(bytes(userData['password'], "utf-8"), salt=salt)
    end = time.perf_counter()

    print("Time for hashing: ", end - st)

    print(USER_TABLE)

    
    
    # try to add the new user, as long as username is unique
    try:
        st=time.perf_counter()

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
        end = time.perf_counter()

        print("Time for db update: ", end - st)


        return True

    except:
        return False



def generateJWT(username):
    expiry = time.time() + 86400
    payload = {
        'username': username, 
        'exp': expiry
        }
    
    encoded = jwt.encode(payload=payload, key=JWT_SECRET, algorithm='HS256')

    return encoded

