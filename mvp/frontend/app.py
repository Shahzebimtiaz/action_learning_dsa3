import streamlit as st
from pages import home, admin #, entity_detail, user_profile, admin, alerts

PAGES = {
    "Home": home
    ,
    # "Entity Detail": entity_detail,
    # "User Profile": user_profile,
    "Admin": admin
    # "Alerts": alerts,
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

page = PAGES[selection]
page.main()





