import numpy as np
import flask
from flask import request, make_response
from qdrant_client import QdrantClient

app = flask.Flask(__name__)

# ------------------------API----------------------------------
# Không cần url và headers nữa vì không gọi API
# url = "https://be12-34-72-112-245.ngrok-free.app"
# headers = {
#     'mssv': '20001955'
# }

# def get_embdding(text):
#     response = requests.post(
#         url + '/embedding', json={'text': text}, headers=headers)
#     return response.json()['embedding']  

# def complete(message, context):
#     response = requests.post(
#         url + '/complete', json={'question': message, 'context': context}, headers=headers)
#     return response.json()

#----------------------------------------------------------------


def get_embedding_random(text):
    # Sinh ngẫu nhiên một vector có chiều dài 1536
    return np.random.rand(1536).tolist()

def complete(message, context):
    # Sinh ngẫu nhiên một chuỗi 100 ký tự
    return {"answer": " ".join([message, " ".join([chr(np.random.randint(97, 123)) for _ in range(100)])])}

def search(query):
    client = QdrantClient(host = "qdrant_db", port = 6333)
    collections = client.get_collections()
    collectionNames = [
        collection.name for collection in collections.collections]
    # embed = get_embdding(query) # Sử dụng hàm của API
    embed = get_embedding_random(query) # Sử dụng hàm mới tạo vector ngẫu nhiên
    if "fit-iuh-news" in collectionNames:
        results = client.search(
            collection_name="fit-iuh-news",
            query_vector=embed,
            limit = 1,
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
        return {"collections": collectionNames}
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
    context = result['payload']['title']+'\n'+result['payload']['content']
    results = complete(query, context)
    print(results)
    return make_response(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5123, debug=False)

# curl -X POST https://localhost:8989/search -H "Content-Type: application/json" -d '{"query": "hội nghị cấp khoa"}'