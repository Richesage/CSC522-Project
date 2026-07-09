from flask import Flask, request, render_template
import pyodbc

app = Flask(__name__)

def search_database(query):
    db_path = r"IR_System.accdb"
    conn_str = r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + db_path + ";"
    results = []
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Using basic SQL for now to get the site wired up
        search_term = f"%{query}%"
        sql = "SELECT Title, Author, Category, PublishYear, Abstract FROM Documents WHERE Title LIKE ? OR Keywords LIKE ? OR Abstract LIKE ?"
        cursor.execute(sql, (search_term, search_term, search_term))
        
        # Convert MS Access rows into a Python list of dictionaries for the webpage
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
            
        cursor.close()
        conn.close()
    except Exception as e:
        print("Database error:", e)
        
    return results

@app.route('/', methods=['GET'])
def home():
    query = request.args.get('query', '')
    results = []
    if query:
        results = search_database(query)
    return render_template('index.html', query=query, results=results)

if __name__ == '__main__':
    # Starts the local web server
    app.run(debug=True)
