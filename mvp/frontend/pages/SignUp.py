import streamlit as st
import requests
import hashlib
from datetime import datetime, timedelta

ADMIN_API_URL_USERS = "http://127.0.0.1:8000/api/v1/endpoints/signup/"
LOGIN_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/login/"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def sign_up():
    st.title("Sign Up")

    today = datetime.today()
    ninety_years_ago = today - timedelta(days=365*90)

    firstname = st.text_input("First Name", key="signup_firstname")
    lastname = st.text_input("Last Name", key="signup_lastname")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
    date_of_birth = st.date_input(
        "Date of Birth",
        value=today.date(),
        min_value=ninety_years_ago.date(),  
        max_value=today.date()  
    )
    gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="signup_gender")

    if st.button("Sign Up"):
        if not firstname:
            st.warning("First Name is required.")
        elif not lastname:
            st.warning("Last Name is required.")
        elif not email:
            st.warning("Email is required.")
        elif not password:
            st.warning("Password is required.")
        elif not confirm_password:
            st.warning("Confirm Password is required.")
        elif not gender:
            st.warning("Gender is required.")
        elif password != confirm_password:
            st.warning("Passwords do not match.")
        else:
            response = requests.post(
                ADMIN_API_URL_USERS,
                json={
                    "firstname": firstname,
                    "lastname": lastname,
                    "email": email,
                    "password": password,
                    "date_of_birth": date_of_birth.isoformat(),
                    "gender": gender
                }
            )
            if response.status_code == 200:
                st.success("You have successfully created an account!")
                #st.session_state['page'] = 'login'
                st.rerun()
            else:
                st.warning(response.json().get("detail", "Something went wrong"))
    
    if st.button("Already have an account? Login"):
        st.session_state['page'] = 'login'
        st.rerun()

def login():
    st.title("Login")
    
    if 'signup_firstname' in st.session_state:
        del st.session_state['signup_firstname']
    if 'signup_lastname' in st.session_state:
        del st.session_state['signup_lastname']
    if 'signup_email' in st.session_state:
        del st.session_state['signup_email']
    if 'signup_password' in st.session_state:
        del st.session_state['signup_password']
    if 'signup_confirm_password' in st.session_state:
        del st.session_state['signup_confirm_password']
    if 'signup_date_of_birth' in st.session_state:
        del st.session_state['signup_date_of_birth']
    if 'signup_gender' in st.session_state:
        del st.session_state['signup_gender']

    email = st.text_input("Email", key="login_email", value="", on_change=None)
    password = st.text_input("Password", key="login_password", type="password", value="", on_change=None)

    if st.button("Login"):
        if not email:
            st.warning("Email is required.")
            return
        elif not password:
            st.warning("Password is required.")
            return
        response = requests.post(
            LOGIN_API_URL,
            json={"email": email, "password": password}
        )
        if response.status_code == 200:
            st.success("Login successful!")
            st.session_state['logged_in'] = True
            st.session_state['page'] = 'home'
            st.rerun()
        else:
            st.warning(response.json().get("detail", "Incorrect email or password"))

    if st.button("Don't have an account? Sign Up"):
        st.session_state['page'] = 'sign-up'
        st.rerun()

def logout():
    st.session_state.clear()
    st.session_state['page'] = 'login'
    st.rerun()


def main():
    st.title("Clinical NER Web App")

    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    page = st.session_state['page']

    if page == "sign-up":
        sign_up()
    elif page == "login":
        login()
    elif page == "home":
        st.write("Welcome to the Home Page")
        if st.button("Logout"):
            logout()

if __name__ == '__main__':
    main()
