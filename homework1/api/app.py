from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flaskext.mysql import MySQL

import openai

app = Flask(__name__)
app.config['SECRET_KEY'] = "ThisIsMySecret"


CORS(app, origins=['http://localhost:3000'])

# Configure MySQL
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Wlf2002.05.21'
app.config['MYSQL_DATABASE_DB'] = 'chatgpt'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL(app)

# Configure the OpenAI API key
openai.api_key = "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"


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/signup', methods=['POST'])
def signup():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    try:
        # Connect to the database
        conn = mysql.connect()
        cursor = conn.cursor()

        # Save the user's sign up information to the database
        sql = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
        cursor.execute(sql, (username, password, email))
        conn.commit()

        # Close the database connection
        cursor.close()
        conn.close()
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

    # Save the user's information in the session
    session['username'] = username
    session['email'] = email

    return jsonify({"success": True, "error": None})


@app.route('/login', methods=['GET', 'POST'])
def login():
    print(request)
    if request.method == 'GET':
        # check if user is in session
        print(session.get('username'))
        username = request.args.get("username")
        if 'username' in session and username in session['username']:
            return jsonify({"username": username, "error": None})
        return jsonify({"username": None, "error": None})

    username = request.json.get('username')
    password = request.json.get('password')

    # TODO: Add code here to check the username and password against the database
    # Return error if it doesn't match 
    try:
        # Connect to the database
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username =%s", [username])
        records = cursor.fetchall() 
        rowCount = len(records) 
        cursor.close()
        conn.close()
        if rowCount != 0:
            db_password = records[0][2]
            if password != db_password:
                return jsonify({"username": None, "error": "Username or password is incorrect."})
        else:
            return jsonify({"username": None, "error": "Username or password is incorrect."})

    # TODO: If the username and password are correct, set the username in the session
    except Exception as e:
        cursor.close()
        conn.close()
        return jsonify({"username": None, "error": str(e)})

    session['username'] = username   
    print("1" + session.get('username'))       
    return jsonify({"username": username, "error": None})


# TODO: Create logout api
# you should retrieve the username from the request, pop it from the session if it's in the session
# then return a result
@app.route("/logout", methods=["POST"])
def logout():
    print('username' in session)
    try:
        username = request.json.get('username')
        if 'username' in session and username == session['username']:
            session.pop('username', None)
            return jsonify({"success": True, "error": None})
        else:      
            return jsonify({"success": False, "error": "username not in session"})
    except Exception as e:
         return jsonify({"success": False, "error": str(e)})

@app.route("/chat", methods=["POST"])
def chat():
    # Get the inputs from the request
    username = request.json["username"]
    question = request.json["question"]

    # Use OpenAI's language generation API to generate a response
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt='You: ' + question,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text

    # Remove the "You: " prefix from the response
    response = response.replace("You: ", "")

    # TODO save the chat history into database
    try:
        # Connect to the database
        conn = mysql.connect()
        cursor = conn.cursor()

        # Save the user's question and chatgpt's answer to the database
        cursor.execute("SELECT id FROM users WHERE username = %s", [username])
        records = cursor.fetchall() 
        user_id = records[0][0]
        sql = "INSERT INTO conversations (user_id, question, answer, timestamp) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (user_id, question, response, "2023/2/19"))

        # Close the database connection
        cursor.close()
        conn.close()

    # TODO: If the username and password are correct, set the username in the session
    except Exception as e:
        cursor.close()
        conn.close()
        return jsonify({"username": None, "error": str(e)})

    # Return the response as JSON
    return jsonify({"response": response})


# TODO: Create chat_history API that returns chat history for the specified user
@app.route("/chat_history", methods=["POST"])
def chat_history():
    username = request.json.get('username')
    try:
        # Connect to the database
        conn = mysql.connect()
        cursor = conn.cursor()

        # Save the user's question and chatgpt's answer to the database
        cursor.execute("SELECT * FROM conversations WHERE user_id = (select id from users where username = %s)", [username])
        records = cursor.fetchall()
        chat_history = [{"input":records[i][2], "output": records[i][3]} for i in range(len(records))]
        
        # Close the database connection
        cursor.close()
        conn.close()
    except Exception as e:
        cursor.close()
        conn.close()
        return jsonify({"success": False, "chat_history": None})
    return jsonify({"success": True, "chat_history": chat_history})



if __name__ == "__main__":
    app.run(debug=True, host='localhost')
