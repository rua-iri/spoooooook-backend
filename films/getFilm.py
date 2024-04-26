import json
import helpers

def lambda_handler(event, context):

    # jwt_token = event['headers'].get('authorization')

    # if not helpers.validateJWT(jwt_token):
    #     return {
    #         'statusCode': 403,
    #         "headers": {"Access-Control-Allow-Origin": "*"},
    #         'body': json.dumps({'error': 'Invalid Authorization Token'})
    #     }


    filmId = event["queryStringParameters"]["imdbID"]

    filmResult = processQuery(filmId)

    return {
        'statusCode': 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        'body': json.dumps(filmResult)
    }



def processQuery(filmId):

    selectQuery = """SELECT film_title, 
                    description, 
                    release_year, 
                    tomato_rating 
                    from film 
                    WHERE imdb_id = (?);"""

    filmResult = helpers.selectQueryDB(selectQuery, (filmId, ), False)
    filmMap = [{"filmTitle": filmResult[0], "filmDescription": filmResult[1], "releaseYear": filmResult[2], "filmRating": filmResult[3]}]

    return filmMap




