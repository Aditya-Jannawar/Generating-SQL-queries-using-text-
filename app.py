# app.py
from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# MySQL Connection
db_config = {
    'host': 'localhost',
    'user': 'root',  # Adjust with your username
    'password': '',  # Adjust with your password
    'database': 'query_builder_db'
}

def get_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fetch_schema', methods=['GET'])
def fetch_schema():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    schema = {}
    for (table_name,) in tables:
        cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        columns = cursor.fetchall()
        schema[table_name] = [column[0] for column in columns]
    
    cursor.close()
    connection.close()
    return jsonify(schema)

@app.route('/generate_query', methods=['POST'])
def generate_query():
    data = request.json
    action = data.get("action")
    query = ""

    if action == "display usernames with document_ids":
        query = """
            SELECT users.username, documents.document_id
            FROM users
            JOIN documents ON users.id = documents.user_id;
        """
    elif action == "display all documents with their titles and user names":
        query = """
            SELECT documents.title, users.username
            FROM documents
            JOIN users ON documents.user_id = users.id;
        """
    elif action == "count the number of documents for each user":
        query = """
            SELECT users.username, COUNT(documents.document_id) AS document_count
            FROM users
            LEFT JOIN documents ON users.id = documents.user_id
            GROUP BY users.username;
        """
    elif action == "display documents created by a specific user":
        query = """
            SELECT documents.title
            FROM documents
            JOIN users ON documents.user_id = users.id
            WHERE users.username = %s;
        """
    elif action == "find users who have more than one document":
        query = """
            SELECT users.username
            FROM users
            JOIN documents ON users.id = documents.user_id
            GROUP BY users.username
            HAVING COUNT(documents.document_id) > 1;
        """
    elif action == "list all document titles containing a specific keyword":
        query = """
            SELECT title
            FROM documents
            WHERE title LIKE %s;
        """
    elif action == "get the most recent document for each user":
        query = """
            SELECT users.username, documents.title, MAX(documents.document_id) AS latest_document
            FROM users
            JOIN documents ON users.id = documents.user_id
            GROUP BY users.username;
        """
    elif action == "display usernames in alphabetical order":
        query = """
            SELECT username
            FROM users
            ORDER BY username ASC;
        """
    elif action == "find the total number of users":
        query = """
            SELECT COUNT(*) AS total_users
            FROM users;
        """
    elif action == "display all users without any documents":
        query = """
            SELECT username
            FROM users
            LEFT JOIN documents ON users.id = documents.user_id
            WHERE documents.document_id IS NULL;
        """
    elif action == "list document titles created after a specific date":
        query = """
            SELECT title
            FROM documents
            WHERE created_date > %s;
        """
    elif action == "find users who have documents with a title length greater than 10 characters":
        query = """
            SELECT DISTINCT users.username
            FROM users
            JOIN documents ON users.id = documents.user_id
            WHERE LENGTH(documents.title) > 10;
        """
    elif action == "get the average number of documents per user":
        query = """
            SELECT AVG(document_count) AS average_documents
            FROM (
                SELECT COUNT(documents.document_id) AS document_count
                FROM users
                LEFT JOIN documents ON users.id = documents.user_id
                GROUP BY users.id
            ) AS user_document_counts;
        """
    elif action == "display document titles and user names for documents with document_id greater than 5":
        query = """
            SELECT documents.title, users.username
            FROM documents
            JOIN users ON documents.user_id = users.id
            WHERE documents.document_id > 5;
        """
    elif action == "find documents for users whose names start with 'A'":
        query = """
            SELECT documents.title
            FROM documents
            JOIN users ON documents.user_id = users.id
            WHERE users.username LIKE 'A%';
        """
    else:
        query = "Unsupported action."

    return jsonify({"query": query})


if __name__ == '__main__':
    app.run(debug=True)
