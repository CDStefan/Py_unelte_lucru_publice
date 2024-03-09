
import streamlit as st
import streamlit_authenticator as stauth
import os

#load the evironment variables
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

# Loading config file
import yaml
from yaml.loader import SafeLoader
with open('src/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Creating the authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'], 
    config['cookie']['key'], 
    config['cookie']['expiry_days'],
    config['preauthorized']
)

hide_bar= """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        visibility:hidden;
        width: 0px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        visibility:hidden;
    }
    </style>
"""

if 'api_key' not in st.session_state:
    st.session_state.api_key = ""


# Creating a login widget
    
try:
    name, autetification_status, username = authenticator.login('main')
except Exception as e:
    st.error(e)

if st.session_state["authentication_status"]:
    authenticator.logout()
    if username == 'petru.ionas':
        st.title('Secțiune utilizator')
        st.write(f'Bine ai venit *{name}*')
        
        st.markdown(
        """
        Aplicația foloseștei interfața API de la OpenAI pentru a genera text.
        Din punct de vedere al securității datelor, acest tip de interogare a modelelor
        îndeplinește standardele europene și internaționale de confidențialitate a datelor.
        ###Mai multe informații despre securitate și auditare se regăsesc la următoarele adrese:
        - Securitate [openai.com/security](https://openai.com/security)
        - Confidențialitate [openai.com/privacy](https://openai.com/enterprise-privacy)
        - Documente de auditare de acces [openai.trust](https://trust.openai.com/)
    
        """
        )

        st.sessio_state.api_key = st.secrets['OPENAI_API_KEY_petru.ionas']
        os.environ['OPENAI_API_KEY'] = st.sessio_state.api_key

    elif username == 'stefan.caravelea':
        st.title('Secțiune administrator')
        st.write(f'Bine ai venit *{name}*')

        st.markdown(
        """
        Aplicația foloseștei interfața API de la OpenAI pentru a genera text.
        Din punct de vedere al securității datelor, acest tip de interogare a modelelor
        îndeplinește standardele europene și internaționale de confidențialitate a datelor.
        ###Mai multe informații despre securitate și auditare se regăsesc la următoarele adrese:
        - Securitate [openai.com/security](https://openai.com/security)
        - Confidențialitate [openai.com/privacy](https://openai.com/enterprise-privacy)
        - Documente de auditare de acces [openai.trust](https://trust.openai.com/)
    
        """
        )
        
        st.sessio_state.api_key = st.secrets['OPENAI_API_KEY_stefan.caravelea']
        os.environ['OPENAI_API_KEY'] = st.sessio_state.api_key



elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
    st.markdown(hide_bar, unsafe_allow_html=True)
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
    st.markdown(hide_bar, unsafe_allow_html=True)

# Creating a password reset widget
if st.session_state["authentication_status"]:
    try:
        if authenticator.reset_password(st.session_state["username"]):
            st.success('Password modified successfully')
    except Exception as e:
        st.error(e)

# Creating a new user registration widget
# try:
#     email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(preauthorization=False)
#     if email_of_registered_user:
#         st.success('User registered successfully')
# except Exception as e:
#     st.error(e)

# Creating a forgot password widget
# try:
#     username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password()
#     if username_of_forgotten_password:
#         st.success('New password sent securely')
#         # Random password to be transferred to the user securely
#     elif username_of_forgotten_password == False:
#         st.error('Username not found')
# except Exception as e:
#     st.error(e)

# Creating a forgot username widget
# try:
#     username_of_forgotten_username, email_of_forgotten_username = authenticator.forgot_username()
#     if username_of_forgotten_username:
#         st.success('Username sent securely')
#         # Username to be transferred to the user securely
#     elif username_of_forgotten_username == False:
#         st.error('Email not found')
# except Exception as e:
#     st.error(e)

# Creating an update user details widget
# if st.session_state["authentication_status"]:
#     try:
#         if authenticator.update_user_details(st.session_state["username"]):
#             st.success('Entries updated successfully')
#     except Exception as e:
#         st.error(e)

# Saving config file
with open('src/config.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)