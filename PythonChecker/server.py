from flask import Flask, render_template, request
#---needed for system calls ---
#import subprocess

app = Flask(__name__)

# Configuration

@app.route('/home', methods=['GET', 'POST'])
def mainIndex():
  
  
  return render_template('home.html')
    
   

  
@app.route('/login', methods=['GET', 'POST'])
def Login():
  global currentUser
  db = utils.db_connect()
  cur = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
  if request.method == 'POST':
    if currentUser == '':
      username = MySQLdb.escape_string(request.form['username'])
      pw = MySQLdb.escape_string(request.form['pw'])
      query = "SELECT * FROM Login AS up INNER JOIN users AS u ON up.L_ID = u.id WHERE u.L_Name = '%s' AND up.password = SHA2('%s',0)" % (username, pw)
      cur.execute(query)
      if cur.fetchone( ):
        currentUser = username
        return redirect(url_for('mainIndex'))
    else:
      warn = "You are already logged in as " + currentUser + "!"
      #return render_template('warning.html', warn = warn)
  return render_template('login.html', curus = currentUser)
  


@app.route('/addProject',methods=['GET','POST'])
def addProject():
  return render_template('addProject.html')


@app.route('/results', methods=['GET', 'POST'])
def results():
   
    return render_template('results.html')
  
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=55200)
	
	
@app.route('editProject', methods = ['POST'])
def editProject():
	db = utils.db_connect()
	cur = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
	
	#get variables from form
	newName = request.form['projName']
	prevName = request.form['prevName']
	inputNum = request.form['inputNum']
	outputNum = request.form['outputNum']
	
	#save project name
	query = "UPDATE Projects SET P_Name='" + newName + "' Where P_Name='" + prevName +"'"
	cur.execute(query) 
	
	#get and save inputs
	for x in range (1, inputNum+1):
		u = 'Input_' + x
		v = 'input' + x
		w = request.form[v]
		
		#check if row exists, add new row if it doesn't
		query = "SELECT EXISTS(SELECT 1 FROM " + newName + " WHERE text LIKE " + u + " LIMIT 1"
		if cur.execute(query):
			query = "UPDATE " + newName + " SET " + u + "=" + w
			cur.execute(query)
		else:
			query = "ALTER TABLE " + newName + " ADD " + u + " varchar(45)"
		
		
	#delete extra inputs
	extraInput = inputNum + 1
	while True:
		u = 'Input_' + extraInput
		
		#check for extra
		query = "SELECT EXISTS(SELECT 1 FROM " + newName + " WHERE text LIKE " + u + " LIMIT 1"
		
		if cur.execute(query):
			query = "ALTER TABLE " + newName + " DROP " + u
			cur.execute
		else:
			break #ends loop if there was no extra
		
		extraInput++
	
	#get and save outputs
	for x in range (1, outputNum+1):
		u = 'Output_' + x
		v = 'output' + x
		w = request.form[v]
		
		#check if row exists, add new row if it doesn't
		query = "SELECT EXISTS(SELECT 1 FROM " + newName + " WHERE text LIKE " + u + " LIMIT 1"
		if cur.execute(query):
			query = "UPDATE " + newName + " SET " + u + "=" + w
			cur.execute(query)
		else:
			query = "ALTER TABLE " + newName + " ADD " + u + " varchar(45)"
		
		
	#delete extra outputs
	extraOutput = outputNum + 1
	while True:
		u = 'Output_' + extraInput
		
		#check for extra
		query = "SELECT EXISTS(SELECT 1 FROM " + newName + " WHERE text LIKE " + u + " LIMIT 1"
		
		if cur.execute(query):
			query = "ALTER TABLE " + newName + " DROP " + u
			cur.execute
		else:
			break #ends loop if there was no extra
		
		extraOutput++
