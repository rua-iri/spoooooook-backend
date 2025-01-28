import json


class Lambda_Response:
    def __init__(self, status_code, status, message):
        self.status_code = status_code
        self.status = status
        self.message = message

    def to_dict(self):
        if self.status_code >= 400:
            message_type = "error"
        else:
            message_type = "message"

        message_content = self.message

        return {
            'statusCode': self.status_code,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                "status": self.status,
                message_type: message_content
            })
        }
