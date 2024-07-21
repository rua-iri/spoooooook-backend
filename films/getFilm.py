import json
import helpers
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def processQuery(filmId):
    try:
        selectQuery = """SELECT film_title,
                        description,
                        release_year,
                        tomato_rating
                        from film
                        WHERE imdb_id = (?);"""

        filmResult = helpers.selectQueryDB(selectQuery, (filmId, ), False)

        if filmResult is None:
            return []

        filmMap = [{
            "filmTitle": filmResult[0],
            "filmDescription": filmResult[1],
            "releaseYear": filmResult[2],
            "filmRating": filmResult[3]
        }]

        return filmMap

    except Exception:
        raise Exception


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

        film_id: str = event["queryStringParameters"].get("imdbID")
        logger.info(f"Film ID: {film_id}")

        if not film_id:
            response.update({'statusCode': 400})
            response.update({
                'body': json.dumps({'status': 'error', 'error': "Film ID required"})
            })
            return response

        film_result = processQuery(film_id)
        logger.info(f"Film Data: {film_result}")

        if not film_result:
            response.update({"statusCode": "404"})
            response.update(
                {'body': json.dumps(
                    {"status": "error", "error": "No results found"}
                )}
            )
            return response

        response.update({'statusCode': 200})
        response.update({
            'body': json.dumps({'status': 'success', 'data': film_result})
        })

        return response

    except Exception as e:
        logger.error(e)
        return response
