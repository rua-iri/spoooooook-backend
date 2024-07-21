import json
import helpers
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def processQuery(filmId):

    try:
        selectQuery = "SELECT film_path from film WHERE imdb_id = (?);"

        filmResult = helpers.selectQueryDB(selectQuery, (filmId, ), False)

        if filmResult is None:
            return []

        return {"filmPath": filmResult[0]}

    except Exception as e:
        raise e


def lambda_handler(event, context):

    # jwt_token = event['headers'].get('authorization')

    # if not helpers.validateJWT(jwt_token):
    #     return {
    #         'statusCode': 403,
    #         "headers": {"Access-Control-Allow-Origin": "*"},
    #         'body': json.dumps({'error': 'Invalid Authorization Token'})
    #     }

    response: dict = {
        'statusCode': 500,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({"status": "error", "error": "internal server error"})
    }

    try:
        filmId: str = event["queryStringParameters"].get("imdbID")

        if not filmId:
            response.update({'statusCode': 400})
            response.update({
                'body': json.dumps({"status": "error", "error": "Film ID required"})
            })
            return response

        filmResult = processQuery(filmId)

        if not filmResult:
            response.update({'statusCode': 404})
            response.update({
                'body': json.dumps({"status": "error", "error": "No results found"})
            })
            return response

        response.update({'statusCode': 200})
        response.update({'body': json.dumps({
            'status': 'success',
            'data': filmResult
        })})

        return response

    except Exception as e:
        logger.error(e)
        return response
