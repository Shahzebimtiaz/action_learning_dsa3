# frontend/pages/admin.py

import streamlit as st
import requests

# URLs for the Admin APIs
ADMIN_API_URL_users = "http://127.0.0.1:8000/api/v1/endpoints/users/"
ADMIN_API_URL_activity = "http://127.0.0.1:8000/api/v1/endpoints/activity_logs/"
TEST_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/test/"

def main():
    st.title("Admin Page")

    tab1, tab2 = st.tabs(["Manage Users", "User Activities"])

    with tab1:
        st.subheader("Manage Users")

        action = st.radio("Choose Action", ["Add User", "Edit User", "Delete User"])

        if action == "Add User":
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            isadmin = st.checkbox("Is Admin")
            if st.button("Add User"):
                response = requests.post(f"{ADMIN_API_URL_users}", json={"email": email, "password": password, "isadmin": isadmin})
                if response.status_code == 200:
                    st.success("User added successfully!")
                else:
                    st.error(f"Error: {response.json()}")

        elif action == "Edit User":
            user_id = st.number_input("User ID", min_value=1)
            email = st.text_input("New Email")
            password = st.text_input("New Password", type="password")
            isadmin = st.checkbox("Is Admin")
            if st.button("Update User"):
                response = requests.put(f"{ADMIN_API_URL_users}{user_id}", json={"email": email, "password": password, "isadmin": isadmin})
                if response.status_code == 200:
                    st.success("User updated successfully!")
                else:
                    st.error(f"Error: {response.json()}")

        elif action == "Delete User":
            user_id = st.number_input("User ID to delete", min_value=1)
            if st.button("Delete User"):
                response = requests.delete(f"{ADMIN_API_URL_users}{user_id}")
                if response.status_code == 200:
                    st.success("User deleted successfully!")
                else:
                    st.error(f"Error: {response.json()}")

        if st.button("Test Endpoint"):
            response = requests.get(TEST_API_URL)
            if response.status_code == 200:
                st.success("Test successful: " + response.json().get("message"))
            else:
                st.error(f"Error: {response.status_code}")

    with tab2:
        st.subheader("User Activities")

        response = requests.get(f"{ADMIN_API_URL_activity}")
        try:
            activities = response.json()
            if not activities:
                st.write("No activities found.")
            else:
                st.write(activities)
        except ValueError:
            st.error("Response is not in JSON format")

if __name__ == "__main__":
    main()
