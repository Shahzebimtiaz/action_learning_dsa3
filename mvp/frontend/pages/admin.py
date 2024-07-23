# # frontend/pages/admin.py

# ##### TO FIX add and update user date of birth #########


# import streamlit as st
# import requests
# import pandas as pd


# # URLs for the Admin APIs
# ADMIN_API_URL_users = "http://127.0.0.1:8000/api/v1/endpoints/users/"
# ADMIN_API_URL_activity = "http://127.0.0.1:8000/api/v1/endpoints/activity_logs/"
# TEST_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/test/"

# def main():
#     st.title("Admin Page")

#     tab1, tab2 = st.tabs(["Manage Users", "User Activities"])

#     with tab1:
#         st.subheader("Manage Users")

#         action = st.radio("Choose Action", ["Add User", "Edit User", "Delete User"])

#         if action == "Add User":
#             firstname = st.text_input("First Name")
#             lastname = st.text_input("Last Name")
#             email = st.text_input("Email")
#             password = st.text_input("Password", type="password")
#             date_of_birth = st.date_input("Date of Birth")
#             gender = st.text_input("Gender")
#             isadmin = st.checkbox("Is Admin")
#             if st.button("Add User"):
#                 date_of_birth_str = date_of_birth.strftime('%Y-%m-%d')
#                 response = requests.post(f"{ADMIN_API_URL_users}", 
#                                          json={"email": email, 
#                                                "password": password,
#                                                "isadmin": isadmin,
#                                                "firstname":firstname,
#                                                "lastname":lastname,
#                                                "date_of_birth":date_of_birth_str,
#                                                "gender": gender })
#                 if response.status_code == 200:
#                     st.success("User added successfully!")
#                 else:
#                     st.error(f"Error: {response.json()}")

#         elif action == "Edit User":
#             user_id = st.number_input("User ID", min_value=1)
#             first_name = st.text_input("New First Name")
#             last_name = st.text_input("New Last Name")
#             email = st.text_input("New Email")
#             password = st.text_input("New Password", type="password")
#             date_of_birth = st.date_input("New Date of Birth (YYYY-MM-DD)")
#             gender = st.text_input("New Gender")
#             isadmin = st.checkbox("Is Admin")
#             if st.button("Update User"):
#                 date_of_birth_str = date_of_birth.strftime('%Y-%m-%d')
#                 response = requests.put(
#                     f"{ADMIN_API_URL_users}{user_id}",
#                     json={
#                         "firstname": first_name,
#                         "lastname": last_name,
#                         "email": email,
#                         "password": password,
#                         "date_of_birth": date_of_birth_str,
#                         "gender": gender,
#                         "isadmin": isadmin
#                     }
#                 )
#                 if response.status_code == 200:
#                     st.success("User updated successfully!")
#                 else:
#                     st.error(f"Error: {response.json()}")

#         elif action == "Delete User":
#             user_id = st.number_input("User ID to delete", min_value=1)
#             if st.button("Delete User"):
#                 response = requests.delete(f"{ADMIN_API_URL_users}{user_id}")
#                 if response.status_code == 200:
#                     st.success("User deleted successfully!")
#                 else:
#                     st.error(f"Error: {response.json()}")


#     with tab2:
#         st.subheader("User Activities")

#         response = requests.get(f"{ADMIN_API_URL_activity}")
#         try:
#             activities = response.json()
#             if not activities:
#                 st.write("No activities found.")
#             else:
#                 # Convert to DataFrame
#                 df = pd.DataFrame(activities)
#                 # Display DataFrame as a table
#                 st.table(df)
#         except ValueError:
#             st.error("Response is not in JSON format")


# if __name__ == "__main__":
#     main()

import streamlit as st
import requests
import pandas as pd

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
            firstname = st.text_input("First Name")
            lastname = st.text_input("Last Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            date_of_birth = st.date_input("Date of Birth")
            gender = st.text_input("Gender")
            isadmin = st.checkbox("Is Admin")
            if st.button("Add User"):
                date_of_birth_str = date_of_birth.strftime('%Y-%m-%d')
                response = requests.post(f"{ADMIN_API_URL_users}", 
                                         json={"email": email, 
                                               "password": password,
                                               "isadmin": isadmin,
                                               "firstname":firstname,
                                               "lastname":lastname,
                                               "date_of_birth":date_of_birth_str,
                                               "gender": gender })
                if response.status_code == 200:
                    st.success("User added successfully!")
                else:
                    st.error(f"Error: {response.json()}")

        elif action == "Edit User":
            user_id = st.number_input("User ID", min_value=1)
            first_name = st.text_input("New First Name")
            last_name = st.text_input("New Last Name")
            email = st.text_input("New Email")
            password = st.text_input("New Password", type="password")
            date_of_birth = st.date_input("New Date of Birth")
            gender = st.text_input("New Gender")
            isadmin = st.checkbox("Is Admin")
            if st.button("Update User"):
                date_of_birth_str = date_of_birth.strftime('%Y-%m-%d')
                response = requests.put(
                    f"{ADMIN_API_URL_users}{user_id}",
                    json={
                        "firstname": first_name,
                        "lastname": last_name,
                        "email": email,
                        "password": password,
                        "date_of_birth": date_of_birth_str,
                        "gender": gender,
                        "isadmin": isadmin
                    }
                )
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

    with tab2:
        st.subheader("User Activities")

        response = requests.get(f"{ADMIN_API_URL_activity}")
        try:
            activities = response.json()
            if not activities:
                st.write("No activities found.")
            else:
                # Convert to DataFrame
                df = pd.DataFrame(activities)
                # Display DataFrame as a table
                st.table(df)
        except ValueError:
            st.error("Response is not in JSON format")

if __name__ == "__main__":
    main()
