import json
import helpers

def lambda_handler(event, context):

    filmId = event["queryStringParameters"]["imdbID"]

    filmResult = processQuery(filmId)

    return {
        'statusCode': 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        'body': json.dumps(filmResult)
    }



def processQuery(filmId):

    selectQuery = "SELECT film_path from film WHERE imdb_id = (?);"

    filmResult = helpers.selectQueryDB(selectQuery, (filmId, ), False)
    filmMap = [{"filmPath": filmResult[0]}]

    return filmMap



