from flask import Flask, request, render_template
import pyodbc

# 1. Safely import scikit-learn components
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    print("\n[ERROR] scikit-learn is not installed. Run 'pip install scikit-learn' in your terminal!\n")

app = Flask(__name__)

def advanced_tfidf_search(query):
    db_path = r"C:\CSC522\IR_System.accdb"
    conn_str = r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + db_path + ";"
    results = []
    
    try:
        # 2. Connect and fetch all 50 records into memory
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT Title, Author, Category, PublishYear, Abstract FROM Documents")
        
        columns = [column[0] for column in cursor.description]
        all_docs = []
        for row in cursor.fetchall():
            all_docs.append(dict(zip(columns, row)))
            
        cursor.close()
        conn.close()
        
        # Guard clause: if database is empty or query is blank
        if not all_docs or not query.strip():
            return []

        # 3. Build the corpus using the Abstract field (handling potential None values safely)
        corpus = [doc['Abstract'] if doc['Abstract'] else "" for doc in all_docs]
        
        # 4. Compute TF-IDF Vectors
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(corpus)
        query_vector = vectorizer.transform([query])
        
        # 5. Calculate similarity scores
        similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()
        
        # 6. Filter and pair scores with documents
        for index, score in enumerate(similarity_scores):
            if score > 0: # Only return documents with an actual match weight
                doc = all_docs[index].copy()
                doc['RelevanceScore'] = round(float(score) * 100, 1) # Convert to percentage
                results.append(doc)
        
        # 7. Sort by relevance ranking (highest score first)
        results = sorted(results, key=lambda x: x['RelevanceScore'], reverse=True)
            
    except Exception as e:
        print("Database or Search processing error:", e)
        
    return results

@app.route('/', methods=['GET'])
def home():
    query = request.args.get('query', '')
    results = []
    if query:
        # We call the new advanced TF-IDF search function here
        results = advanced_tfidf_search(query)
    return render_template('index.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)