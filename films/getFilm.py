import json
import secretstuff
import mysql.connector

def lambda_handler(event, context):

    filmId = event["queryStringParameters"]["imdbID"]

    filmResult = mysqlSelectQuery(filmId)

    return {
        'statusCode': 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        'body': json.dumps(filmResult)
    }



def mysqlSelectQuery(filmId):

    # connect to database and execute query
    mydb = mysql.connector.connect(
        host=secretstuff.hostName,
        user=secretstuff.userName,
        password=secretstuff.passwordName,
        database=secretstuff.databaseName,
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT film_title, description, release_year, tomato_rating from film WHERE imdb_id = '" + filmId + "';")
    filmResult = mycursor.fetchone()

    filmMap = [{"filmTitle": filmResult[0], "filmDescription": filmResult[1], "releaseYear": filmResult[2], "filmRating": filmResult[3]}]

    return filmMap




