from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL



app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe' # set a secret key for security purposes

@app.route('/')
def index():
    mysql = connectToMySQL("first_flask")
    friends = mysql.query_db("SELECT * FROM friends;") 
    return render_template("index.html", all_friends = friends)

@app.route('/process', methods=['POST'])
def process():
    is_valid = True		# assume True
    if len(request.form['fname']) < 1:
    	is_valid = False
    	flash("Please enter a first name")
    if len(request.form['lname']) < 1:
    	is_valid = False
    	flash("Please enter a last name")
    if len(request.form['occ']) < 2:
    	is_valid = False
    	flash("Occupation should be at least 2 characters")
    
    if not is_valid:    # if any of the fields switched our is_valid toggle to False
    #Above can also be writted as ----> if not '_flashes' in session.keys():	# no flash messages means all validations passed
        return redirect('/')    # redirect back to the method that displays the index page
    else:               # if is_valid is still True, all validation checks were passed
        mysql = connectToMySQL("first_flask")
        query = "INSERT INTO friends(first_name, last_name, occupation, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(occup)s, NOW(), NOW());"
        data = {
            "fn": request.form["fname"],
            "ln": request.form["lname"],
            "occup": request.form["occ"],
        }
        new_friend_id = mysql.query_db(query, data)
        flash("Friend successfully added!")
        return redirect("/")    # eventually we may have a different success route

if __name__=="__main__":
    app.run(debug=True)