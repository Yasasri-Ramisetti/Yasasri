from flask import Flask , request, jsonify
import psycopg2
from psycopg2 import sql

app= Flask(__name__)

#database configuration 
DB_HOST='localhost'
DB_NAME='postgres'
DB_USER='postgres'
DB_PASSWORD='2226'
def get_db_connection():
    connection = psycopg2.connect(
        host= DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return connection

def create_tb_if_not_exist():
    connection=get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_db(
                student_id SERIAL PRIMARY KEY,
                student_name   TEXT NOT NULL,
                course_code TEXT NOT NULL,
                course_name TEXT NOT NULL,
                roll_no TEXT NOT NULL,
                email TEXT NOT NULL                     
            );
    """)
    connection.commit()
    cursor.close()
    connection.close()   

create_tb_if_not_exist ()
@app.route("/student_register",methods=['POST'])
def user_register():
    student_name =request.json['student_name']
    course_code=request.json['course_code']
    course_name=request.json['course_name']
    roll_no=request.json['roll_no']
    email=request.json['email']
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("""
          INSERT INTO student_db(student_name,course_code,course_name,roll_no,email)
          VALUES(%s, %s, %s, %s, %s)
    """ ,(student_name,course_code,course_name,roll_no,email))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message":"user registered successfully"}),200

@app.route("/get_student",methods=['GET'])
def get_student():
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("""
            SELECT * FROM student_db;       
""")  
    student_db=cursor.fetchall()
    cursor.close()
    connection.close()
    result=[
        { "student_id": student[0], 
          "student_name": student[1], "course_code": student[2],"course_name":student[3],"roll_no":student[4],"email":student[5]} for student in student_db
        
    ]
    return jsonify(result), 200

@app.route('/student_update', methods=['PUT'])
def student_update():
    student_id = request.args.get('student_id')
    student_name = request.json['student_name']
    course_code = request.json['course_code']
    course_name = request.json['course_name']
    roll_no = request.json['roll_no']
    email = request.json['email']

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE student_db
        SET student_name = %s, course_code = %s, course_name = %s, roll_no = %s,email = %s
        WHERE student_id = %s;
    """, (student_name, course_code, course_name, roll_no, email, student_id))

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "user update successfully"}), 201

@app.route("/delete_student",methods=['DELETE'])
def delete_student():
    student_id = request.args.get('student_id')
    connection=get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        DELETE FROM student_db WHERE student_id=%s;
    """,(student_id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "user deleted successfully"}), 200



if __name__=="__main__":
        app.run(debug=True)