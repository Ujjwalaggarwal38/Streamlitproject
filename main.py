import streamlit as st
import sqlite3
from streamlit_option_menu import option_menu

def connectdb():
    conn = sqlite3.connect("mydb.db")
    return conn
def createTable():
    with connectdb() as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS student(name text,password text,roll int primary key,branch text)")
        conn.commit()
def addRecord(data):
    with connectdb() as conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO student(name,password,roll,branch) VALUES(?,?,?,?)",data)
            conn.commit()
        except sqlite3.IntegrityError:
            st.error("Student already registerd")
def display():
    with connectdb() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM student")
        result = cur.fetchall()
        return result

def signup():
    st.title("Registration Page")
    name = st.text_input("Enter Name")
    password = st.text_input("Enter Password", type='password')
    repassword = st.text_input("Retype your Password ", type='password')
    roll = st.number_input("Enter Roll Number",format="%0.0f")
    branch = st.selectbox("Enter Branch",options=["CSE","AIML","IT","ECE",'ME'])
    if st.button('SignIn'):
        if password !=repassword:
            st.warning("Password Mismatch")
        else:
            addRecord((name,password,roll,branch))
            st.success("Student Registered !!!!")
            
createTable()            
with st.sidebar:
    # st.sidebar.image('./images/brain.ico')
    selected = option_menu("My App", ['Signup','Display All record'])

if selected == 'Signup':
    signup()
else:
   data = display()
   st.table(data)
