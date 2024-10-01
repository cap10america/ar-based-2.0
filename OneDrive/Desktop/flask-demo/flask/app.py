from flask import Flask, request, jsonify, render_template , redirect , url_for ,flash
import mysql.connector
from database import db_config 
import hashlib
import re


   


def hash_password(password):    
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password
  # hash_password()
  


def get_db_connection():

    return mysql.connector.connect(**db_config)

def validate_email(email):
  """Validates an email address using regular expression.

  Args:
    email: The email address to validate.

  Returns:
    True if the email is valid, False otherwise.
  """

  # Simplified regular expression pattern
  email_regex = r"^\w+@\w+\.\w{2,4}$"

  # Check if the email matches the pattern
  if re.match(email_regex, email):
    return True
  else:
    return False









app = Flask(__name__)



@app.route('/')
def index():
    return render_template('signup.html')
  
# @app.route('/signup',methods=["POST","GET"])
# def signup():
#   if request.method =='POST' :
#     conn = get_db_connection()
#     mycommand =conn.cursor()
#     name =request.form.get('institute_name')
#     mobile =request.form.get('mobile')
#     email=request.form.get('email')
#     username =request.form.get('username')
#     password =request.form.get('password')
#     address =request.form.get('address')
#     contact_details =request.form.get('contact_details')
#     query="insert into institute_registration (email ,name , mobile , username , password , address , contact_details) values ( %s , %s , %s , %s , %s , %s , %s)" 
#     mycommand.execute(query ,( email , name , mobile , username , password , address , contact_details , ))
#     conn.commit()
#     mycommand.close()
#     conn.close()

#     return jsonify({"message ":" succesfull registration "})
  
    
    

# @app.route('/signup', methods=['POST'])
# def signup():
#    if request.method =='POST' :
    
#       try:
#           conn = get_db_connection()
#           mycommand =conn.cursor()
#           email = request.form['email']
#           name = request.form['institute_name']
#           mobile = request.form['mobile']
#           username = request.form['username']
#           password = request.form['password']
#           address = request.form['address']
#           contact_details = request.form['contact_details']

#           query = "INSERT INTO institute_registration (email, name, mobile, username, password, address, contact_details) VALUES (%s, %s, %s, %s, %s, %s, %s)"
#           mycommand.execute(query, (email, name, mobile, username, password, address, contact_details))
#           conn.commit()
#           mycommand.close()
#           conn.close()
#           return jsonify({'message':'registration successfull'})
#           # return redirect(url_for('login'))
#       except mysql.connector.errors.IntegrityError as e:
#           # Handle the IntegrityError
#           error_message = "Error occurred while signing up. Please check the form data and try again."
#           return render_template('signup.html', error=error_message)
#       except Exception as e:
#           # Handle other exceptions
#           error_message = "An unexpected error occurred. Please try again later."
#           return render_template('signup.html', error=error_message)

    

@app.route('/signup', methods=['POST' ,"GET"])
# def signup():  
  # flash('Signup successful!', 'success')
  
def institute_register():
    if request.method =='POST' :
        conn =get_db_connection()
        mycommand =conn.cursor()
        institute =request.form.get('institute_name')
        email =request.form.get('email')
        mobile=request.form.get('mobile')
        username =request.form.get('username')
        password =request.form.get('password')
        address =request.form.get('address')
        contact_details =request.form.get('contact_details')        
        if all([institute ,email ,mobile ,username ,password ,address ,contact_details]):
          if validate_email(email) :
              
            query = "select * from institute_registration where email =%s "
            mycommand.execute(query ,(email ,))
            result =mycommand.fetchall()
            if result :
                return jsonify({'status_code':400 ,'message' :"the email already  exists"})
            else :
                query ="select * from institute_registration where name =%s"
                mycommand.execute(query ,(institute ,) )
                exists=mycommand.fetchall()
                if exists :
                    return jsonify({'status_code':400 ,'message':"the institute name already exists"})               
                
                else :
                  query ="select * from institute_registration where username =%s"
                  mycommand.execute(query ,(username ,))
                  is_exists =mycommand.fetchall()
                  if is_exists :
                      return jsonify({'status_code':400 ,'message':"username already exists "})
                      
                  else :
                    query ="insert into institute_registration ( name ,email ,mobile ,username ,password ,address ,contact_details ) values(%s ,%s ,%s ,%s ,%s ,%s , %s )"
                    mycommand.execute(query ,(institute , email ,mobile ,username , password,address ,contact_details,))
                    # mycommand.execute("INSERT INTO institute_registration (email, mobile, username, password, address, contact_details) VALUES (%s, %s, %s, %s, %s, %s)", (email, mobile, username, password, address, contact_details ,))
                    conn.commit()
                    mycommand.close()
                    conn.close()
                    return render_template('succes.html')
                    # return jsonify({'status_code':201 ,'message':"the institute registration successfully"})
                    # return redirect(url_for('succes'))
                  # jsonify({'status_code':201,'redirecting':render_template('sigin.html')})
          else :
            return jsonify({'status_code':400,'message':"enter a valid email"})
            
            
        else :
            return jsonify({'status_code':404,'message':"the missing arguments"})
          
          
    # return "error message"
        
    if request.method =='GET' :
        conn=get_db_connection()
        mycommand=conn.cursor()
        query ="select * from institute_registration "
        mycommand.execute(query)
        result =mycommand.fetchall()
        if result :
            return jsonify({'status_code':200 ,'message':result})
        else :
            return jsonify({'status_code':400, 'message':'no records'})

#   print("signup successfull")  

# return render_template('signin.html')

# @app.route('/signin')
# def signin():
#   # flash('Signin  successful!', 'success')  
#   print("signup successfull") 

  
#   return "thanqks for singing in our website"

# # @app.route('/')
# # def index():
# #     return render_template('signup.html')

@app.route('/succes')
def signin():
  return render_template('signin.html')

@app.route('/signin',methods=['POST','GET'])
def signup():
  if request.method=="POST":
     conn =get_db_connection()
     mycommand =conn.cursor()        
     email =request.form.get('email')  
     password =request.form.get('password')          
     if all([ email , password ]):
       
       if validate_email(email) :
         query ="select * from institute_registration where email= %s and password =%s "
         mycommand.execute(query ,(email ,password , ))
         exists=mycommand.fetchall()
         if exists :
           return render_template('index.html', data  =exists)
         else :
           conn.close()
           mycommand.close()
           
           return jsonify({'message':'invalid credentials '})
           
       else :
          return jsonify({'message':'invalid email ...!'})  
         
     else :
       return jsonify({'message':'invalid arguments'})    
    
    
  return render_template('succes.html')



# # @app.route('/succes')
# # def succes():
# #   return render_template('signin')
  

# # @app.route('/succes')
# # def succes():
# #   return redirect(url_for('signin'))
  




# @app.route('/index')
# def getUser_data():
#     conn =get_db_connection()
#     mycommand =conn.cursor()        
#     email =request.form.get('email')  
#     password =request.form.get('password')    
    
#     # query ="select * from institute_registration where email= %s and password =%s "
#     # mycommand.execute(query ,(email ,password ))
#     # exists=mycommand.fetchall()
#     # if exists :
#     query = "SELECT * FROM institute_registration WHERE email = %s AND password = %s"
#     mycommand.execute(query, (email, password ,))
#     exists = mycommand.fetchall()  # Fetch all rows

#           # Convert list of tuples to list of dictionaries
#     columns = [desc for desc in mycommand.description]
#     data = [dict(zip(columns, row)) for row in exists]

#     if data:
#       return render_template('index.html' ,data = data )
#     else :
#       conn.close()
#       mycommand.close()
      
#       return jsonify({'message':'invalid credentials '})





@app.route('/index', methods=['POST', 'GET'])
def getdata():
    if request.method == "POST":
        conn = get_db_connection()
        mycommand = conn.cursor()  # Standard cursor
        email = request.form.get('email')
        password = request.form.get('password')

        if email and password:
            if validate_email(email):
                query = "SELECT * FROM institute_registration WHERE email = %s AND password = %s"
                mycommand.execute(query, (email, password))
                exists = mycommand.fetchone()  # Fetch all rows

                # Convert list of tuples to list of dictionaries
                columns = [desc for desc in mycommand.description]
                data = [dict(zip(columns, row)) for row in exists]

                if data:
                    conn.close()
                    mycommand.close() 
                    return render_template('index.html', content ="exists")
                    # return redirect('siginsuccess.html')
                else:
                    conn.close()
                    mycommand.close()
                    return jsonify({'message': 'Invalid credentials'}), 401
            else:
                return jsonify({'message': 'Invalid email format'}), 400
        else:
            return jsonify({'message': 'Email and password are required'}), 400

    return render_template('signin.html')
 



if __name__ == '__main__':

  
  app.run(debug=True)