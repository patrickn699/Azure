from flask import Flask, render_template, redirect, url_for, request, jsonify
import os, base64
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['APP_MODE'] = os.getenv('APP_MODE', 'development')  # Default to 'development' if not set
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL', 'sqlite:///:memory:')  # Default DB URL if not set
app.config['API_KEY'] = os.getenv('API_KEY', 'default-api-key')  

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'password')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'content_db')

# Initialize MySQL
mysql = MySQL(app)

data_file_path = os.path.join(os.getcwd(), 'flask_basic/files', 'storage.txt') #'files/storage.txt'

# Route for the homepage
@app.route('/')
def home():

    # cur = mysql.connection.cursor()
    # cur.execute("CREATE TABLE IF NOT EXISTS content_table (id INT AUTO_INCREMENT PRIMARY KEY, content TEXT)")
    # cur.execute("SELECT content FROM content_table ORDER BY id DESC LIMIT 1")
    # content_row = cur.fetchone()
    # content = content_row[0] if content_row else "No content found. Create some content by visiting /update."
    # cur.close()

    if os.path.exists(data_file_path):
        with open(data_file_path, 'r') as file:
            content = file.read()
    else:
        content = "No content found. Create some content by visiting /update."

    return render_template('home.html',app_mode=app.config['APP_MODE'],
                           database_url=app.config['DATABASE_URL'],
                           api_key=app.config['API_KEY'],
                           content=content,
                           mysql_db= app.config['MYSQL_DB'],
                           mysql_host= app.config['MYSQL_HOST'],
                           mysql_user = app.config['MYSQL_USER'],
                           mysql_pass = app.config['MYSQL_PASSWORD'])





@app.route('/sql')
def sqlhome():

    new_content = request.form.get('content', 'Default content')

    try:
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS content_table (id INT AUTO_INCREMENT PRIMARY KEY, content TEXT)")
            #cur.execute("INSERT INTO content_table (content) VALUES(new_content)")
            #cur.execute("INSERT INTO content_table (content) VALUES (%s)", (new_content,))
            cur.execute("SELECT content FROM content_table ORDER BY id DESC LIMIT 1")
            content_row = cur.fetchone()
            content = content_row[0] if content_row else "No content found. Create some content by visiting /update."
            cur.close()

        return render_template('home.html',app_mode=app.config['APP_MODE'],
                           database_url=app.config['DATABASE_URL'],
                           api_key=app.config['API_KEY'], content=content,
                           mysql_db= app.config['MYSQL_DB'],
                           mysql_host= app.config['MYSQL_DB'],
                           mysql_user = app.config['MYSQL_USER'])
    
    except:

        return jsonify({"message": "somthing went wrong", "new_content": new_content})



    



@app.route('/update', methods=['POST'])
def update_content():
    # Get the content to save from the request (or use default)
    new_content = request.form.get('content', 'Default content')

    # Save the new content to the file in the persistent volume
    try:
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO content_table (content) VALUES (%s)", (new_content,))
            mysql.connection.commit()
            cur.close()

        with open(data_file_path, 'w') as file:
            file.write(new_content)

        return jsonify({"message": "Content saved successfully", "new_content": new_content,"path":data_file_path})

    except:
        os.makedirs(os.path.dirname(data_file_path), exist_ok=True)
        f = open(data_file_path, "w")
        f.write(new_content)
        return jsonify({"message": "file does not exist, so created one, but not in db!","path":data_file_path})





    


# Route for the second page
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
