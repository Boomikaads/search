from flask import Flask, request, jsonify, redirect, render_template
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb+srv://kavi22021ad:Kaviya1234@cluster0.jyx09.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['Constitution']
collection = db['articles']

# Serve the index.html file
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')

    aggregate_query = [
        {
            "$search": {
                "text": {
                    "query": query,
                    "path": ["content", "title", "topic"]
                },
                "highlight": {
                    "path": ["content", "title", "topic"]
                }
            }
        },
        {
            "$project": {
                "article_number": 1,
                "title": 1,
                "content": 1,
                "topic": 1,
                "score": {"$meta": "searchScore"},
                "highlights": {"$meta": "searchHighlights"}
            }
        }
    ]

    results = list(collection.aggregate(aggregate_query))

    response = []
    for result in results:
        response.append({
            "topic": result.get("topic", "No topic"),
            "title": result.get("title", "No Title"),
            "content": result.get("content", "No Content"),
            "highlights": result.get("highlights", [])
        })

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)

