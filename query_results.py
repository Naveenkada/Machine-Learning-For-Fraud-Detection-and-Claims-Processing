import sqlite3
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Database file path
DATABASE = 'insurance_claims.db'

# Insert blockchain data into the database
def insert_blockchain_data(chain):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    for block in chain:
        cursor.execute('''
            INSERT INTO blockchain ("index", previous_hash, proof, timestamp, transactions)
            VALUES (?, ?, ?, ?, ?)
        ''', (block['index'], block['previous_hash'], block['proof'], block['timestamp'], str(block['transactions'])))
    conn.commit()
    conn.close()

# Route to store the blockchain data
# @app.route('/store-chain', methods=['POST'])
def store_chain():
    blockchain_data = request.json
    chain = blockchain_data.get("chain")
    if chain:
        insert_blockchain_data(chain)
        return jsonify({"message": "Blockchain data stored successfully!"}), 201
    else:
        return jsonify({"message": "No blockchain data provided!"}), 400

# Route to retrieve blockchain data
# @app.route('/get-chain', methods=['GET'])
def get_chain():
    conn = sqlite3.connect(DATABASE)
    df = pd.read_sql_query('SELECT * FROM blockchain', conn)
    conn.close()
    return df.to_json(orient='records')

if __name__ == '__main__':
    get_chain()
    app.run(debug=True)
