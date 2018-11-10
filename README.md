# PoetsHaven
Search from a repository of over 300 poems!!

## Deployment

1. Make sure you have Python 3.5 ,Django 1.11 and Bootstrap 4 installed.
2. Start the Django server with the command \
        `python3.5 manage.py runserver`
3. Navigate to _http://127.0.0.1:8000/search_ in your web server.
4. Click on refresh. This will create the database.\
**Note**: This is to be done **only the first time**.
5. Type the query of your choice and hit _Search!!_

## Features

1. Uses Vector Space model for documents and queries, using cosine distance between queries and documents to measure similarity for ranking.
2. WordNet lemmatizer used for stemming the documents.
2. Spelling correction.
3. Also Supports phrase queries.

## Screenshots
### Query example 1:
![query 1](https://github.com/PrajwalRavi/PoetsHaven/blob/master/Samples/shakes.png)

### Query example 2:
![query 2](https://github.com/PrajwalRavi/PoetsHaven/blob/master/Samples/roses.png)

### Result:
![result](https://github.com/PrajwalRavi/PoetsHaven/blob/master/Samples/result.png)

### Phrase query:
![phrase](https://github.com/PrajwalRavi/PoetsHaven/blob/master/Samples/phrase%20query.png)

### Spelling correction:
![spell](https://github.com/PrajwalRavi/PoetsHaven/blob/master/Samples/spell.png)
