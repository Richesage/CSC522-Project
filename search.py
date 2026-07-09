import pyodbc

# 1. Hardcode the full path to the .accdb file
# Example: r"C:\xampp\htdocs\IR_System.accdb" or r"C:\Users\YourName\Desktop\IR_System.accdb"
db_path = r"C:\Users\DELL\Documents\Academics\Part 5 First Semester\Second Semester\CSC522 Project Assignment\IR_System.accdb"

# 2. Establish the connection string
conn_str = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    f"DBQ={db_path};"
)
# ... [Keep the rest of your try/except block the same] ...

try:
    # 3. Connect to the database
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    print("Successfully connected to the MS Access database!")
    
    # 4. Run a test search query (looking for 'learning')
    search_term = "%learning%"
    sql = "SELECT Title, Author FROM Documents WHERE Title LIKE ? OR Abstract LIKE ?"
    
    cursor.execute(sql, (search_term, search_term))
    results = cursor.fetchall()
    
    print(f"\nFound {len(results)} results:")
    for row in results:
        print(f"- {row.Title} by {row.Author}")
        
    # Clean up connections
    cursor.close()
    conn.close()

except pyodbc.Error as e:
    print("Error connecting to the database:")
    print(e)