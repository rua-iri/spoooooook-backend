import json


class Lambda_Response:
    def __init__(self, status_code, status, message):
        self.status_code = status_code
        self.status = status
        self.message = message

    def to_dict(self):
        if self.status_code >= 400:
            message: dict = {"error": self.message}
        else:
            message: dict = {"message": self.message}

        return {
            'statusCode': self.status_code,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                "status": self.status,
                message
            })
        }
