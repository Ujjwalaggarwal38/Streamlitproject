import streamlit as st
import sqlite3
def connectdb():
    conn = sqlite3.connect("mydb.db")
    return conn
def createTable():
    with connectdb() as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS student(name text,password text,roll int primary key,Branch text)")
        conn.commit()
        
def add_record(data):
    st.error(data)
def uiSignup():
    st.title("Sign Up Form")
    name = st.text_input("Enter Name ")
    pw = st.text_input("Enter password ",type = "password")
    repw = st.text_input("Re-Enter password ",type = "password")
    roll = st.number_input("Enter roll number ")
    branch = st.selectbox("Branch",options = ["CSE","ECE","AIML"])
    if st.button('Signin'):
        if pw!=repw:
            st.warning("Password Mismatch ")
        else:
            add_record((name,pw,roll,branch))
            st.success("Student registered !!!")
def reset():
    st.title("RESET PASSWORD")
    roll = st.number_input("Enter roll number ")
    with connectdb() as conn:
        cur = conn.cursor()
        cur.execute(f"select password from student where roll = {roll}")
        m = cur.fetchone()    
        pw = st.text_input("Enter New password ",type = "password")
        repw = st.text_input("Re-Enter password ",type = "password")
        if st.button('Reset Password'):
            if pw!=repw:
                st.warning("Password Mismatch ")
            else:
                cur.execute(f"update student set password = {pw} where roll = {roll}")
                con.commmit()
                st.success("Student registered !!!")
        
    
createTable()
uiSignup()
#reset()