
import requests
import flask
from flask import request, make_response
from qdrant_client import QdrantClient

app = flask.Flask(__name__)

url = "https://7f60-34-80-120-251.ngrok-free.app"
headers = {
    "mssv": "20001955"
}


def get_embedding(text):
    response = requests.post(
        url + "/embedding", json={"text": text}, headers=headers)
    return response.json()['embedding']


def complete(message, context):
    response = requests.post(
        url + "/complete", json={"question": message, "content": context}, headers=headers)
    return response.json()


def search(query):
    client = QdrantClient(host="qdrant_db", port=6333)
    collections = client.get_collections()
    collectionNames = [
        collection.name for collection in collections.collections]
    embed = get_embedding(query)
    if "fit-iuh-news" in collectionNames:
        results = client.search(
            collection_name="fit-iuh-news",
            query_vector=embed,
            limit=1,
        )
        return results[0].model_dump()
    return {"message": "Collection not found"}


@app.route('/get_collections', methods=['GET'])
def get_collections():
    client = QdrantClient(host="qdrant_db", port=6333)
    collections = client.get_collections()
    collectionNames = [
        collection.name for collection in collections.collections]
    if collectionNames:
        return make_response({"collections": str(collectionNames)})
    else:
        return {"message": "No collection in database"}


@app.route('/search', methods=['POST'])
def searchView():
    query = request.json['query']
    results = search(query)
    return make_response(results)


@app.route('/complete', methods=['POST'])
def completeView():
    query = request.json['query']
    result = search(query)
    context = result["payload"]['title']+"\n"+result["payload"]['content']
    results = complete(query, context)
    print(results)
    return make_response(results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5123, debug=False)

# curl -X POST http://localhost:8989/search -H "Content-Type: application/json" -d '{"query": "hội nghị cấp khoa"}'
