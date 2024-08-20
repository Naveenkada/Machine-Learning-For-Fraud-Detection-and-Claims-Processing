from flask import Flask, render_template, request, redirect, jsonify, url_for  ,send_file
import sqlite3  
import pandas as pd  
from blockchain.blockchain import Blockchain  

app = Flask(__name__)  
blockchain = Blockchain()  

# Database file path  
DATABASE = 'insurance_claims.db'  

# Helper function to fetch distinct values from the database  
def get_dropdown_values(column_name):  
    with sqlite3.connect(DATABASE) as conn:  
        cursor = conn.cursor()  
        cursor.execute(f'SELECT DISTINCT {column_name} FROM claims')  
        results = [row[0] for row in cursor.fetchall()]  
    return results  

# Insert blockchain data into the database  
def insert_blockchain_data(chain):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        for block in chain:
            # Check if the block with the same index already exists
            cursor.execute('SELECT 1 FROM blockchain WHERE "index" = ?', (block['index'],))
            exists = cursor.fetchone()
            
            if exists:
                # Update the block if it exists
                cursor.execute('''
                    UPDATE blockchain
                    SET previous_hash = ?, proof = ?, timestamp = ?, transactions = ?
                    WHERE "index" = ?
                ''', (block['previous_hash'], block['proof'], block['timestamp'], str(block['transactions']), block['index']))
            else:
                # Insert the block if it doesn't exist
                cursor.execute('''
                    INSERT INTO blockchain ("index", previous_hash, proof, timestamp, transactions)
                    VALUES (?, ?, ?, ?, ?)
                ''', (block['index'], block['previous_hash'], block['proof'], block['timestamp'], str(block['transactions'])))
        
        conn.commit()


# Route to render the insurance claims form  
@app.route('/')  
def index():  
    policy_states = get_dropdown_values('policy_state')  
    policy_csls = get_dropdown_values('policy_csl')  
    insured_sexes = get_dropdown_values('insured_sex')  
    insured_education_levels = get_dropdown_values('insured_education_level')  
    insured_occupations = get_dropdown_values('insured_occupation')  
    insured_hobbies = get_dropdown_values('insured_hobbies')  

    return render_template(  
        'index.html',  
        policy_states=policy_states,  
        policy_csls=policy_csls,  
        insured_sexes=insured_sexes,  
        insured_education_levels=insured_education_levels,  
        insured_occupations=insured_occupations,  
        insured_hobbies=insured_hobbies  
    )  

# Route to handle insurance claims form submission  
@app.route('/submit-claim', methods=['POST'])  
def submit_claim():  
    data = request.form  
    with sqlite3.connect(DATABASE) as conn:  
        cursor = conn.cursor()  
        cursor.execute('''  
            INSERT INTO claims (months_as_customer, age, policy_state, policy_csl, policy_deductable,   
                                policy_annual_premium, umbrella_limit, insured_sex, insured_education_level,   
                                insured_occupation, insured_hobbies, capital_gains, capital_loss)  
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  
        ''', (  
            data['months_as_customer'], data['age'], data['policy_state'], data['policy_csl'],  
            data['policy_deductable'], data['policy_annual_premium'], data['umbrella_limit'],   
            data['insured_sex'], data['insured_education_level'], data['insured_occupation'],   
            data['insured_hobbies'], data['capital_gains'], data['capital_loss']  
        ))  
        conn.commit()  
        # Add the claim to the blockchain  
        form_data = data.to_dict()  # Converts the form data to a dictionary  
        blockchain.new_transaction(form_data)  
        proof = blockchain.proof_of_work(blockchain.last_block['proof'])  
        blockchain.new_block(proof)  
        # Store the blockchain data  
        insert_blockchain_data(blockchain.chain)  
    
        
    
    return redirect(url_for('thank_you'))  

# Route to display thank you page  
@app.route('/thank_you')  
def thank_you():  
    return """  
    <!DOCTYPE html>  
    <html lang="en">  
    <head>  
        <meta charset="UTF-8">  
        <meta name="viewport" content="width=device-width, initial-scale=1.0">  
        <title>Thank You</title>  
        <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">  
        <style>  
            /* General Reset */  
            * {  
                margin: 0;  
                padding: 0;  
                box-sizing: border-box;  
                font-family: Arial, sans-serif;  
            }  
    
            /* Body Style */  
            body {  
                background-color: #f4f4f4;  
                color: #333;  
                line-height: 1.6;  
                margin: 20px;  
                text-align: center;  
                padding: 50px 0;  
            }  
            
            /* Header Style */  
            h2 {  
                color: #4CAF50;  
                font-size: 2rem;  
                margin-bottom: 20px;  
            }  
            
            /* Paragraph Style */  
            p {  
                font-size: 18px;  
                color: #555;  
                margin-bottom: 30px;  
            }  
            
            /* Button Styles */  
            .button {  
                text-decoration: none;  
                color: white;  
                background-color: #007BFF;  
                padding: 10px 20px;  
                border-radius: 5px;  
                margin: 10px;  
                display: inline-block;  
                transition: background-color 0.3s;  
            }  
            
            .button:hover {  
                background-color: #0056b3;  
            }  
        </style>  
    </head>  
    <body>  
        <h2>Thank You!</h2>  
        <p>Your claim has been successfully submitted and added to the blockchain.</p>  
        <div>  
            <a href="/download_chain" download class="button">Download Chain Key Details</a>  
            <a href="/claims" class="button">View Claims</a>  
            <a href="/view_chains" class="button">View Chains</a>  
             <a href="/" class="button">Return to Home</a>  
        </div>  
    </body>  
    </html>  
    """
# Route to store the blockchain data    

# Route to retrieve blockchain data  
@app.route('/get_chain', methods=['GET'])  
def get_chain():  
    with sqlite3.connect(DATABASE) as conn:  
        df = pd.read_sql_query('SELECT * FROM blockchain', conn)  
    return df.to_json(orient='records')  
# Route to display the blockchain chain  
@app.route('/get_chain')  
def full_chain():  
    """Retrieves the full blockchain and inserts it into the database.  

    Returns:  
        JSON response containing the blockchain and its length.  
    """  
    # Create a response dictionary with the chain and its length  
    response = {  
        'chain': blockchain.chain,  
        'length': len(blockchain.chain),  
    }  
    # Prepare the JSON response  
    chain_data = jsonify(response)  
    
    # Insert the blockchain data into the SQLite database  

    return chain_data

# Route to display submitted claims  
@app.route('/claims')  
def display_claims():  
    with sqlite3.connect(DATABASE) as conn:  
        cursor = conn.cursor()  
        cursor.execute("SELECT * FROM claims WHERE policy_csl <> '78' ORDER BY ID DESC")  
        claims = cursor.fetchall()  
    return render_template('claims.html', claims=claims)  


@app.route('/view_chains')  
def view_chains():  
    with sqlite3.connect(DATABASE) as conn:  
        df = pd.read_sql_query('SELECT b.*, c.id FROM blockchain b LEFT JOIN claims c ON c.id = b.[index]', conn) 
    
    # Convert DataFrame to a list of dictionaries  
    blockchain_data = df.to_dict(orient='records')  
    return render_template('view_chains.html', blockchain=blockchain_data)

@app.route('/download_chain', methods=['GET'])  
def download_chain():  
    with sqlite3.connect(DATABASE) as conn:  
        # Get the blockchain data from the SQLite database  
        df = pd.read_sql_query('SELECT * FROM blockchain', conn)  
    
    # Convert the data to JSON format  
    json_data = df.to_json(orient='records', indent=4)  

    # Write JSON data to a text file  
    file_path = 'blockchain_data.txt'  
    with open(file_path, 'w') as f:  
        f.write(json_data)  

    # Send the file to the user for download  
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':  
    app.run(debug=True)