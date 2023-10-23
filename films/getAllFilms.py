import json
import helpers


def lambda_handler(event, context):

    filmGenre = event["queryStringParameters"]["category"]

    filmResults = processQuery(filmGenre)

    return {
        'statusCode': 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        'body': json.dumps(filmResults)
    }



def processQuery(filmCategory):
    resultsList = []

    selectQuery = """SELECT film.imdb_id, 
                    poster_path 
                    FROM category 
                    INNER JOIN film_category 
                    ON category.category_id = film_category.category_id 
                    INNER JOIN film ON film_category.film_id = film.film_id 
                    WHERE category.category_title=(?);"""
    
    allResults = helpers.selectQueryDB(selectQuery, (filmCategory, ), True)
    



    # append each result to the results list
    for singleResult in allResults:
        filmMap = {"imdbID": singleResult[0], "posterPath": singleResult[1]}
        resultsList.append(filmMap)

    return resultsList

