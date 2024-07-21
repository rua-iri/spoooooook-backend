import json
import helpers
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def processQuery(filmCategory):
    try:
        results_list: list = []

        select_query: str = """SELECT film.imdb_id,
                        poster_path
                        FROM category
                        INNER JOIN film_category
                        ON category.category_id = film_category.category_id
                        INNER JOIN film ON film_category.film_id = film.film_id
                        WHERE category.category_title=(?);"""

        all_results: list = helpers.selectQueryDB(
            select_query,
            (filmCategory, ),
            True
        )

        # append each result to the results list
        for singleResult in all_results:
            filmMap = {
                "imdbID": singleResult[0],
                "posterPath": singleResult[1]
            }

            results_list.append(filmMap)

        return results_list
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

    response_body: dict = {
        'statusCode': 500,
        "headers": {"Access-Control-Allow-Origin": "*"},
        'body': json.dumps({"status": "error", "error": "internal server error"})
    }

    try:

        print(event)

        film_genre: str = event["queryStringParameters"]["category"]
        logger.info(f"Film Genre: {film_genre}")

        # ensure that film genre is provided
        if not film_genre:
            response_body.update({"statusCode": "400"})
            response_body.update(
                {'body': json.dumps(
                    {"status": "error", "error": "Category is required"})
                 }
            )
            return response_body

        # query for films in this genre
        film_results: list = processQuery(film_genre)

        if not film_results:
            response_body.update({"statusCode": "404"})
            response_body.update(
                {'body': json.dumps(
                    {"status": "error", "error": "No results found"}
                )}
            )
            return response_body

        response_body.update({'statusCode': 200})
        response_body.update(
            {'body': json.dumps({
                "status": "success",
                "data": film_results
            })})

        return response_body

    except Exception as e:
        logger.error(e)
        return response_body
