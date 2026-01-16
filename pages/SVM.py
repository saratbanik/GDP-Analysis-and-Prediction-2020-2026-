import streamlit as st
from PIL import Image
st.markdown("# SVM")
st.sidebar.markdown('''
# Performance
## `Selected features and scaling`
    - MAE: 7040.04
    - RMSE: 9794.59
    - R2 Score: -0.16
''')


# @st.cache_data
def login(username,password):
    database = {'vilas':'vilas','smruthi':'smruthi','rishith':'rishith','rohan':'rohan'}
    if username in database.keys():
        if database[username]!=password:
            st.error('Username/password did not match ')
            st.stop()
        else:
            st.session_state['username']=username
            return True

if 'username' not in st.session_state:
    with st.expander("Please fill the below credentials to begin",expanded=True):
        with st.form("login"):
            # st.write("Please with the credentials to login")
            username=st.text_input('Enter the username','',placeholder='username')
            psw=st.text_input('Enter the password','',placeholder='password',type='password')
            # Every form must have a submit button.
            submitted = st.form_submit_button("Login",type='secondary',use_container_width=True)
        if submitted:
            login(username,psw)
            

        if not username or not psw:
            st.warning('Please do login before perform any operation')
            st.stop()



image = Image.open('SVM.jpg')

st.image(image, caption='Test data vs Prediction',use_column_width=True)

with open("SVM.jpg", "rb") as file:
    btn = st.download_button(
            label="Download image",
            data=file,
            file_name="SVM.jpg",
            mime="image/jpg",
            
            use_container_width=True
          )


st.error('''
### Feature scaling and selection did not help much for the prediction in our case, hence results of SVM is worse than Linear Regression. 
''')

st.markdown('### Compared with Random Forest Regression')
col1, col2, col3 = st.columns(3)
col1.metric("MAE", "7040.04", "-15.33")
col2.metric("RMSE", "9794.59", "0.01")
col3.metric("R2 Score", "-0.16", "-1")

st.info('MAE and RMSE should be lower for high performance & R2 score should be greater',icon='ℹ️')
