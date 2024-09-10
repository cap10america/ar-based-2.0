from flask import Flask, request, jsonify, render_template , redirect , url_for
import hashlib
import os
from werkzeug.utils import secure_filename


# # from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

import mysql.connector

# # from app.database import db_config
# # ,JWT_SECRET_KEY
from  database import db_config




# app = Flask(__name__)







# # Configure the Flask app with a secret key for JWT

# # app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

def get_db_connection():

    return mysql.connector.connect(**db_config)

        

    
    





# # # Function to hash the password (replace with your chosen hashing algorithm)
def hash_password(password):    
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password









app = Flask(__name__)
app.config['UPLOAD_FOLDER'] ='uploads/'

# @app.route('/')
# def register_form():
#   return render_template("register.html")

# @app.route('/register', methods=['POST'])

# def register():
#   try :
#     name = request.form.get('name')
#     email = request.form.get('email')
#     password = request.form.get('password')
#     phone = request.form.get('phone')
    
    
#     if all([name,email,password,phone]) :
#       conn=get_db_connection()
#       mycommand=conn.cursor()
#       user="show tables like 'user'"
#       mycommand.execute(user)
#       Is_user =mycommand.fetchone()
#       if Is_user :
#         exists ="select * from user where username =%s "
#         mycommand.execute(exists ,(name ,))
#         Is_exists =mycommand.fetchone()
#         if Is_exists :
#           mycommand.close()
#           conn.close()        
#           return "the  user already exists",400
        
        
#         query ="insert into user (username ,email,password ,phone) values (%s,%s,%s,%s)"
#         mycommand.execute( query, (name ,email , hash_password(password) , phone) )
#         conn.commit()
#         mycommand.close()
#         conn.close()
#         return f" {name} registered successfully"
        
      
#       else :
#         mycommand.close()
#         conn.close()
#         return "user table does not exists ",404
      
      
#     else : 
      
#       return " missing arguments ""status_code",404
#   except :
#     return "error"  
# @app.route('/register',methods=['POST'])
# def login_data():
#   conn =get_db_connection()
#   mycommand =conn.cursor()
#   name = request.form.get('username')
  
#   Is_user =""
#   mycommand.close()




@app.route('/')
def index():
  return render_template('demo.html')  

@app.route('/demo',methods=['POST'])
def register():
   mail = request.form.get('email')
   password = request.form.get('password')
   return render_template('upload.html' )


@app.route('/upload',methods=['POST'])
def upload_file():
  conn =get_db_connection()
  mycommand=conn.cursor()
  file = request.files.get('file')

  if file and file.filename:  
    file_data = file.read()  # Read file data as binary
  
    filename =secure_filename(file.filename)
    file_path =os.path.join(app.config['UPLOAD_FOLDER'],filename)
    file.save(file_path)

    # query ="insert into image (image) values (%s)"
    # query ="insert into images (image) values (%s)"
    mycommand.execute("INSERT INTO images (image) VALUES (%s)", (file_data,))


    
    # mycommand.execute(query,(filename,))
    # mycommand.execute("INSERT INTO image (image) VALUES (%s)", (filename,))
    conn.commit()
    mycommand.close()
    conn.close()
    return "successs upload the image in database"
  
  return "error nosuch file selected or file is empty ",404
  
  


  # Process or store data here (e.g., print to console)
#   message = f"You registered successfully! Name: {name}, Email: {email}"
#   return render_template("register.html", message=message)

if __name__ == '__main__':
  if not os.path.exists(app.config['UPLOAD_FOLDER']) :
    os.makedirs(app.config['UPLOAD_FOLDER'])
  
  app.run(debug=True)