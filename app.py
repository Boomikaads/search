from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection setup (ensure your credentials are correctly formatted)
client = MongoClient("mongodb+srv://kavi22021ad:Kaviya1234@cluster0.jyx09.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['Constitution']
collection = db['articles']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')

    # If the query is empty, return an error
    if not query:
        return jsonify({"error": "Search query cannot be empty"}), 400

    aggregate_query = [
        {
            "$search": {
                "text": {
                    "query": query,
                    "path": ["content", "title", "topic"]  # Searching across specified fields
                },
                "highlight": {
                    "path": ["content", "title", "topic"]  # Highlighting the relevant fields
                }
            }
        },
        {
            "$project": {
                "article_number": 1,  # Include article number
                "title": 1,           # Include title
                "content": 1,         # Include content
                "topic": 1,           # Include topic
                "score": {"$meta": "searchScore"},  # Search score for ranking relevance
                "highlights": {"$meta": "searchHighlights"}  # Highlighted snippets
            }
        }
    ]

    # Execute the aggregation query
    results = list(collection.aggregate(aggregate_query))
    
    # Formatting the response to return relevant details and highlights
    response = []
    for result in results:
        response.append({
            "article_number": result.get("article_number", "N/A"),  # Include article number
            "topic": result.get("topic", "No topic"),
            "title": result.get("title", "No Title"),
            "content": result.get("content", "No Content"),
            "highlights": result.get("highlights", [])  # Add highlights if available
        })
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)


