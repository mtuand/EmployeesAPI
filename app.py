from flask import Flask, request
from flask_mysqldb import MySQL
from flask import jsonify

app = Flask(__name__)

try:
  app.config['MYSQL_HOST'] = 'localhost'
  app.config['MYSQL_USER'] = 'root'
  app.config['MYSQL_PASSWORD'] = '' #Default password for MySQL
  app.config['MYSQL_DB'] = 'Company' 
  mysql = MySQL(app)

except:
  print "Error logging into MySQL"

"""
Root endpoint which supports a GET request that pulls all Employees in the database Company as a collection 
of json. Also supports a POST request that adds a new employee to the db in json format:
{id:, name:, email:, category:}.
"""
@app.route('/', methods=['GET','POST'])
def main():
  if(request.method == 'GET'):
    try:
      cur = mysql.connection.cursor()
      resultVal = cur.execute("SELECT * FROM Employees")
      results = []
      if resultVal > 0:
        allEmployees = cur.fetchall()
        for employee in allEmployees:
          results.append({"Id":employee[0],
                          "Name": employee[1],
                          "Email":employee[2],
                          "Category":employee[3]})
        return jsonify(results), 200;
    
    except:
      return 404;
  
  elif(request.method == 'POST'):
    try:
        jsonInput = request.get_json()
        idnum = jsonInput['Id']
        name = jsonInput['Name']
        email = jsonInput['Email']
        category = jsonInput['Category']
        
        cur = mysql.connection.cursor()
        
        resultVal = cur.execute("SELECT * FROM Employees WHERE id = %s", (str(idnum)))
        if resultVal == 0:
          cur.execute("INSERT INTO Employees(id,name,email,category) VALUES(%s,%s,%s,%s)"
                      , (idnum, name, email, category))
          mysql.connection.commit()
          cur.close()
          return jsonify(jsonInput), 201;
        else:
          return "Id already exists.", 404;
    
    except:
      return 404;

"""
Endpoint that supports a GET request to pull information up for an individual employee based on id in db.
"""
@app.route('/employees/<idnum>', methods=['GET'])
def getId(idnum):
  try:
      cur = mysql.connection.cursor()
      resultVal = cur.execute("SELECT * FROM Employees WHERE id = %s", idnum)
      if resultVal > 0:
        employee = cur.fetchone()
        return jsonify({"Id":employee[0],
                        "Name": employee[1],
                        "Email":employee[2],
                        "Category":employee[3]}), 200;
      else:
        return "Not Found.", 404;
  
  except:
    return 404;
  
"""
Endpoint for managing employees. Supports Deleting employees from db and updating employee info based on id.
"""
@app.route('/employees', methods=['PUT', 'DELETE'])
def manage():
  if(request.method == 'PUT'):
    try:
      jsonInput = request.get_json()
      
      idnum = str(jsonInput['Id'])
      name = str(jsonInput['Name'])
      email = str(jsonInput['Email'])
      category = str(jsonInput['Category'])
      
      cur = mysql.connection.cursor()
      resultVal = cur.execute(
                        "SELECT * FROM Employees WHERE id = %s", (idnum))
      if resultVal > 0:
        cur.execute("UPDATE Employees SET name = %s, email = %s, category = %s WHERE id = %s"
                        , (name, email, category, idnum))
        mysql.connection.commit()
        cur.close()
        return jsonify(jsonInput),200;
      else:
        return "Not found.", 404;
    except:
      return 405;
  
  elif(request.method == 'DELETE'):
    try:
      jsonInput = request.get_json()
      
      idnum = str(jsonInput['Id'])
      name = str(jsonInput['Name'])
      email = str(jsonInput['Email'])
      category = str(jsonInput['Category'])

      cur = mysql.connection.cursor()
      resultVal = cur.execute(
                        "SELECT * FROM Employees WHERE id = %s AND name = %s AND email = %s AND category = %s"
                        , (idnum, name, email, category))
      if resultVal > 0:
        cur.execute("DELETE FROM Employees WHERE id = %s AND name = %s AND email = %s AND category = %s"
                        , (idnum, name, email, category))
        mysql.connection.commit()
        cur.close()
        return jsonify(jsonInput),200;
      
      else:
        return "Not found.", 404;
    
    except:
      return 405;

if __name__ == '__main__':
  app.run(debug=True);