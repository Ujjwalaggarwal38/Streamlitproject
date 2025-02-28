import streamlit as st
import sqlite3
from streamlit_option_menu import option_menu

def connectdb():
    conn = sqlite3.connect("mydb.db")
    return conn

def createTable():
    with connectdb() as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS student(name text, roll int primary key, branch text, password text)")
        conn.commit()

def add_record(data):
    with connectdb() as conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO student(name, roll, branch, password) VALUES (?, ?, ?, ?)", data)
            conn.commit()
        except sqlite3.IntegrityError:
            st.error("Student already registered")

def display(search_query=None):
    with connectdb() as conn:
        cur = conn.cursor()
        query = "SELECT * FROM student WHERE 1=1"
        
        if search_query:
            query += f" AND (name LIKE '%{search_query}%' OR roll LIKE '%{search_query}%')"

        cur.execute(query)
        result = cur.fetchall()
        return result

def display1(branch_filter=None):

    with connectdb() as conn:
        cur = conn.cursor()
        query = "SELECT * FROM student WHERE 1=1"
        
        if branch_filter:
            query += f" AND branch='{branch_filter}'"
        cur.execute(query)
        result = cur.fetchall()
        return result


def reset_password():
    st.title("Reset Password")
    roll = st.number_input("Enter your Roll Number", format="%0.0f")
    new_password = st.text_input("Enter New Password", type='password')
    confirm_password = st.text_input("Confirm New Password", type='password')

    if st.button("Reset Password"):
        if new_password != confirm_password:
            st.warning("Passwords do not match!")
        else:
            with connectdb() as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM student WHERE roll=?", (roll,))
                result = cur.fetchone()
                if result:
                    cur.execute("UPDATE student SET password=? WHERE roll=?", (new_password, roll))
                    conn.commit()
                    st.success("Password successfully updated!")
                else:
                    st.error("Roll number not found!")

def UI_Signup():
    st.title("REGISTRATION FORM")
    name = st.text_input("ENTER YOUR NAME")
    branch = st.selectbox("ENTER YOUR BRANCH", options=["CSE", "AIML", "ME", "CE"])
    roll = st.number_input("ENTER YOUR ROLL NO.", format="%0.0f")
    password = st.text_input("ENTER YOUR PASSWORD", type='password')
    repassword = st.text_input("RE-ENTER YOUR PASSWORD", type='password')
    
    if st.button("SignIn"):
        if password != repassword:
            st.warning("Password Mismatched")
        else:
            add_record((name, roll, branch, password))
            st.success("*Student Registered*")

def UI_Search():
    st.title("Search")    

    search_query = st.text_input("Search by Name or Roll No.")

    data = display(search_query=search_query)
    
    if data:
        st.table(data)
    else:
        st.info("No students found matching the criteria.")

def UI_Filter():
    st.title("Filter Using Branch")    

    branch_filter = st.selectbox("Filter by Branch", options=["All", "CSE", "AIML", "ME", "CE"])
    if branch_filter == "All":
        branch_filter = None
    data = display1(branch_filter=branch_filter)
    if data:
        st.table(data)
    else:
        st.info("No students found matching the criteria.")


def delete_student():
    st.title("Delete Student Record")
    roll = st.number_input("Enter the Roll Number of the student to delete", format="%0.0f")

    if st.button("Delete Student"):
        with connectdb() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM student WHERE roll=?", (roll,))
            result = cur.fetchone()
            if result:
                cur.execute("DELETE FROM student WHERE roll=?", (roll,))
                conn.commit()
                st.success(f"Student with Roll Number {roll} has been deleted.")
            else:
                st.error("Roll number not found!")

createTable()

with st.sidebar:
    selected = option_menu("My App", ['Signup', 'Display', 'Reset Password', 'Search','Filter Using Branch', 'Delete Student'], 
                           icons=['box-arrow-in-right', 'table', 'key', 'search','filter', 'trash'], 
                           default_index=0)

if selected == 'Signup':
    UI_Signup()
elif selected == 'Reset Password':
    reset_password()
elif selected == 'Search':
    UI_Search()
elif selected == 'Filter Using Branch':
    UI_Filter()   
elif selected == 'Delete Student':
    delete_student()
else:
    data = display()
    st.table(data)
