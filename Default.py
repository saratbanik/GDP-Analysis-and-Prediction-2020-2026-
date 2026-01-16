import streamlit as st 
import pickle
from streamlit_option_menu import option_menu
import numpy as np
import time
import pandas as pd
import plotly.express as px
from datetime import date





# Implementing the design

st.set_page_config(
    page_title="GDP Prediction & Analysis",
    page_icon="random",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'About': "# Made by SARAT BANIK!"
    }
)
# Loading the saved Random Forest model

@st.cache_resource(show_spinner=True)
def get_model(model_name):
    model = pickle.load(open(model_name,'rb'))
    return model
@st.cache_resource(show_spinner=True)
def get_data(name):
    data=pd.read_csv(name)
    return data

RFmodel=get_model('RFmodel.pkl')
data=get_data('filtered_data.csv')

# ------------------LOGIN---------------------------
st.title("GDP ANALYSIS AND PREDICTION")



import streamlit as st
import bcrypt
import sqlite3

# st.session_state['username']=''
def create_user_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 username TEXT NOT NULL, 
                 password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def signup():
    if 'username' in st.session_state and   len(st.session_state['username'])>0:
        st.success(f"Hey {st.session_state['username'].capitalize()}, you are logged in already")
        isLog=True
        return

    st.write("Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    confirm_password = st.text_input("Confirm Password", type='password')

    if st.button("Signup",type='primary',use_container_width=True):
        if password == confirm_password:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()
            st.success("You have successfully created an account!")
            st.info("Please login to proceed.")
        else:
            st.warning("Passwords do not match.")

def login():
    # session = get(username='')
    if 'username' in st.session_state and len(st.session_state['username'])>0:
        st.write("### Hey",':blue[', st.session_state.username.capitalize()+' 👋',']')
        isLog=True
        return

    st.write("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login",type='primary',use_container_width=True):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        result = c.fetchone()
        conn.close()
        if result:
            hashed_password = result[2]
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                st.session_state['username'] = username
                st.success("You have successfully logged in!")
                isLog=True
            else:
                st.warning("Incorrect Password")
                st.stop()
        else:
            st.markdown("## :red[Username not found, Please Sign Up!]")
            st.stop()

def logout():
    
    if len(st.session_state['username'])<=0:
        st.warning("You have not logged in yet!")
        return

    st.session_state['username'] = ''
    st.success("You have successfully logged out!")




def main():
    isLog = False
    create_user_table()


    menu = ["Login", "Signup", "Logout"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "Signup":
        signup()
    elif choice == "Login":
        login()
    elif choice == "Logout":
        logout()

if __name__ == '__main__':
    main()


# hide = True
# # @st.cache_data
# def login(username,password):
#     database = {'vilas':'vilas','smruthi':'smruthi','rishith':'rishith','rohan':'rohan'}
#     if username in database.keys():
#         if database[username]!=password:
#             st.error('Username/password did not match ')
#             st.stop()
#         else:
#             st.session_state['username']=username
#             hide=False
#             return True

# def auth(hide):
#     if 'username' not in st.session_state:
#         with st.expander("Please fill the below credentials to begin",expanded=hide):
#             with st.form("login"):
#                 # st.write("Please with the credentials to login")
#                 username=st.text_input('Enter the username','',placeholder='username')
#                 psw=st.text_input('Enter the password','',placeholder='password',type='password')
#                 # Every form must have a submit button.
#                 submitted = st.form_submit_button("**LOGIN**",type='primary',use_container_width=True)
#             if submitted:
#                 hide=False
#                 login(username,psw)
#                 return True
#             if not username or not psw:
#                 st.warning('Please do login before performing any operation')
#                 st.stop()

# if 'username' not in st.session_state:
#     auth(hide=True)
# else:
#     auth(hide=False)





# st.write(st.session_state.username)
if 'username' in st.session_state and  len(st.session_state['username'])>0:
    st.sidebar.title('Hi :blue['+ st.session_state.username.capitalize()+'!]')

else:
    st.stop()    

with st.sidebar:
    selected = option_menu(
        menu_title="Main menu",
        options=["Prediction","Analytics","Recommendation","Help"],
        
    )
st.header(f"{selected}")


# -------------------------------Prediction-----------------------------------------

if selected == 'Prediction':
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
        latest_iteration.text(f'App is getting ready... {i+1}%')
        bar.progress(i + 1)
        time.sleep(0.01)
    
    tab1,tab2 = st.tabs(["Global", "India"])



        
    with tab1:

        st.markdown('''
        :orange[Disclaimer]
        
            Feel free to change the values to predict GDP per capita of any Region!''')

        # INPUT VALUES FROM THE USER
        
        cc1,cc2,cc3 = st.columns(3)
        
        att_popl = st.number_input('Population (Example: 7000000)', min_value=1e4, max_value=2e9, value=2e7)

        ac1,ac2= st.columns(2)
        with ac1:
            att_area = st.slider('Area (sq. Km)', min_value= 2.0, max_value= 17e6, value=6e5, step=1e4)
        with ac2:
            att_cost = st.slider('Coastline/Area Ratio', min_value= 0, max_value= 800, value=30, step=10)
        att_dens = st.slider('Population Density (per sq. mile)', min_value= 0, max_value= 12000, value=400, step=10)

        att_migr = st.slider('Annual Net Migration (migrant(s)/1,000 population)', min_value= -20, max_value= 25, value=0, step=2) 
        att_mort = st.slider('Infant mortality (per 1000 births)', min_value= 0, max_value=195, value=40, step=10)
        att_litr = st.slider('Population literacy Percentage', min_value= 0, max_value= 100, value=80, step=5)
        att_phon = st.slider('Phones per 1000', min_value= 0, max_value= 1000, value=250, step=25)
        
        
        with cc1:
            att_arab = st.slider('Arable Land (%)', min_value= 0, max_value= 100, value=25, step=2)
        with cc2:
            att_crop = st.slider('Crops Land (%)', min_value= 0, max_value= 100, value=5, step=2)
        with cc3:
            att_othr = st.slider('Other Land (%)', min_value= 0, max_value= 100, value=70, step=2)
        st.markdown('`Arable, Crops, and Other land are summed up to 100%`')

        #Climate
        att_clim = st.selectbox('Climate', options=('Mostly hot (like: Egypt and Australia)', 'Mostly hot and Tropical (like: China and Cameroon)', 'Mostly cold and Tropical (like: India)', 'Mostly cold and Tropical (like: India)', ' Mostly cold (like: Argentina and Belgium)'))
        if att_clim == 'Mostly hot (like: Egypt and Australia)':
            att_clim=1
        elif att_clim == 'Mostly hot and Tropical (like: China and Cameroon)':
            att_clim=1.5
        elif att_clim == 'Mostly tropical (like: The Bahamas and Thailand)':
            att_clim=2
        elif att_clim == 'Mostly cold and Tropical (like: India)':
            att_clim=2.5
        elif att_clim == 'Mostly cold (like: Argentina and Belgium)':
            att_clim=3

        cc1,cc2 = st.columns(2)
        with cc1:
            att_brth = st.slider('Annual Birth Rate (births/1,000)', min_value= 7, max_value= 50, value=20, step=2)
        with cc2:
            att_deth = st.slider('Annual Death Rate (deaths/1,000)', min_value= 2, max_value= 30, value=10, step=2)
        
        cc1,cc2,cc3 = st.columns(3)
        with cc1:
            att_agrc = st.slider('Agricultural Economy', min_value= 0.0, max_value= 1.0, value=0.15, step=0.05)
        with cc2:
            att_inds = st.slider('Industrial Economy', min_value= 0.0, max_value= 1.0, value=0.25, step=0.05)
        with cc3:
            att_serv = st.slider('Services Economy', min_value= 0.0, max_value= 1.0, value=0.60, step=0.05)
        st.markdown('`Agricultural, Industrial, and Services Economy are summarized to 1`')
        att_regn = st.selectbox('Region', options=('ASIA (EX. NEAR EAST)','BALTICS','C.W. OF IND. STATES','EASTERN EUROPE','LATIN AMER. & CARIB','NEAR EAST','NORTHERN AFRICA','NORTHERN AMERICA','OCEANIA','SUB-SAHARAN AFRICA','WESTERN EUROPE'))

        if att_regn == "ASIA (EX. NEAR EAST)":
            att_regn = 1
        elif att_regn == "BALTICS":
            att_regn = 2
        elif att_regn == "C.W. OF IND. STATES":
            att_regn = 3
        elif att_regn == "EASTERN EUROPE":
            att_regn = 4
        elif att_regn == "LATIN AMER. & CARIB":
            att_regn = 5
        elif att_regn == "NEAR EAST":
            att_regn = 6
        elif att_regn == "NORTHERN AFRICA":
            att_regn = 7
        elif att_regn == "NORTHERN AMERICA":
            att_regn = 8
        elif att_regn == "OCEANIA":
            att_regn = 9
        elif att_regn == "SUB-SAHARAN AFRICA":
            att_regn = 10
        elif att_regn == "WESTERN EUROPE":
            att_regn = 11


        if att_regn == 1:
            att_regn_1 = 1
            att_regn_2 = att_regn_3 = att_regn_4 = att_regn_5 = att_regn_6 = att_regn_7 = att_regn_8 = att_regn_9 = att_regn_10 = att_regn_11 = 0
        elif att_regn == 2: 
            att_regn_2 = 1
            att_regn_1 = att_regn_3 = att_regn_4 = att_regn_5 = att_regn_6 = att_regn_7 = att_regn_8 = att_regn_9 = att_regn_10 = att_regn_11 = 0
        elif att_regn == 3: 
            att_regn_3 = 1
            att_regn_1 = att_regn_2 = att_regn_4 = att_regn_5 = att_regn_6 = att_regn_7 = att_regn_8 = att_regn_9 = att_regn_10 = att_regn_11 = 0
        elif att_regn == 4: 
            att_regn_4 = 1
            att_regn_1 = att_regn_3 = att_regn_2 = att_regn_5 = att_regn_6 = att_regn_7 = att_regn_8 = att_regn_9 = att_regn_10 = att_regn_11 = 0
        elif att_regn == 5: 
            att_regn_5 = 1
            att_regn_1 = att_regn_3 = att_regn_4 = att_regn_2 = att_regn_6 = att_regn_7 = att_regn_8 = att_regn_9 = att_regn_10 = att_regn_11 = 0
        elif att_regn == 6: 
            att_regn_6 = 1
            att_regn_1 = att_regn_3 = att_regn_4 = att_regn_5 = att_regn_2 = att_regn_7 = att_regn_8 = att_regn_9 = att_regn_10 = att_regn_11 = 0
        elif att_regn == 7: 
            att_regn_7 = 1
            att_regn_1 = att_regn_3 = att_regn_4 = att_regn_5 = att_regn_6 = att_regn_2 = att_regn_8 = att_regn_9 = att_regn_10 = att_regn_11 = 0
        elif att_regn == 8: 
            att_regn_8 = 1
            att_regn_1 = att_regn_3 = att_regn_4 = att_regn_5 = att_regn_6 = att_regn_7 = att_regn_2 = att_regn_9 = att_regn_10 = att_regn_11 = 0
        elif att_regn == 9: 
            att_regn_9 = 1
            att_regn_1 = att_regn_3 = att_regn_4 = att_regn_5 = att_regn_6 = att_regn_7 = att_regn_8 = att_regn_2 = att_regn_10 = att_regn_11 = 0
        elif att_regn == 10: 
            att_regn_10 = 1
            att_regn_1 = att_regn_3 = att_regn_4 = att_regn_5 = att_regn_6 = att_regn_7 = att_regn_8 = att_regn_9 = att_regn_2 = att_regn_11 = 0
        else: 
            att_regn_11 = 1
            att_regn_1 = att_regn_3 = att_regn_4 = att_regn_5 = att_regn_6 = att_regn_7 = att_regn_8 = att_regn_9 = att_regn_10 = att_regn_2 = 0


        user_input = np.array([att_dens, att_migr, 
                            att_mort, att_litr, att_phon, 
                                att_brth, att_agrc, att_serv, 
                                att_regn_1, att_regn_2, att_regn_3,
                            att_regn_4, att_regn_5, att_regn_6, att_regn_7, 
                            att_regn_8, att_regn_9, att_regn_10, att_regn_11]).reshape(1,-1)

        # st.write(user_input.shape)

        if (st.button('__**Predict GDP**__',use_container_width=True,type='primary')):
            prediction=RFmodel.predict(user_input)

            with st.spinner('Prediction is on the way...'):
                time.sleep(2)


            with st.container( ):
                st.balloons()
                st.snow()
                st.header(f'The estimated GDP per capita is: `{float(prediction)}` ')
                st.success(f'R2 Score of the _Random Forest Regressor_ is: __{0.84}__')
                st.info('Generally R2 score __>0.7__ is considered as good', icon="ℹ️")

    with tab2:
        from sklearn.model_selection import train_test_split, GridSearchCV
        from sklearn.metrics import r2_score
        from sklearn.linear_model import LinearRegression
        from sklearn.ensemble import RandomForestRegressor
        st.write('## What do you want to predict?')

        target  = st.selectbox('Target attribute',
             options=(
            
            'GDP growth (annual %)','Population, total', 'Population growth (annual %)',
       'Life expectancy at birth, total (years)',
        'Inflation, GDP deflator (annual %)',
       'Agriculture, forestry, and fishing, value added (% of GDP)',
       'Industry (including construction), value added (% of GDP)',
       'Exports of goods and services (% of GDP)',
       'Imports of goods and services (% of GDP)',
       'Foreign direct investment, net inflows (BoP, current US$)'
        ))
        # year = st.slider('In how many years from 2020?', step=1,min_value=1,max_value=100,help='We take years from 2020')
        
        # Splitting dataset
        df=pd.read_csv('./India/IndData.csv')
        
        train =np.asarray(df.drop(['Year','Military expenditure (% of GDP)', 'Merchandise trade (% of GDP)',target],axis=1))
        test=np.asarray(df[target])
        X_train, X_test, y_train, y_test = train_test_split(train, test, test_size=0.33, random_state=2)
        
        rgr = LinearRegression()
        rgr.fit(X_train,y_train)
        pred=rgr.predict(X_test)
        # Select a single row from the X_test dataset
        x_new = X_test[0, :]  # assumes X_test is a pandas DataFrame

        # Reshape the data to a 2D array with shape (1, n_features)
        x_new = x_new.reshape((1, -1))
        pred=rgr.predict(x_new)
        st.markdown(f'''
        # The Predicted :orange[{target}] is :green[{   format(pred[0].round(3),',') } { 'bn' if target=='Population, total' else '$' if target=='Foreign direct investment, net inflows (BoP, current US$)' else '%' } ]

        >   Based on data till 2020 using Linear Regression
        ''')

        from sklearn.tree import DecisionTreeRegressor
        regressor = DecisionTreeRegressor(random_state=0)
        regressor.fit(X_train, y_train)
        l=regressor.predict(X_test, check_input=True)

        rf = RandomForestRegressor(random_state=42)
        # param_grid = {
        #     "n_estimators": [10, 50, 100],
        #     "max_depth": [None, 5, 10],
        #     "min_samples_split": [2, 5, 10],
        # }
        # grid_search = GridSearchCV(rf, param_grid, cv=5, scoring="r2")
        rf.fit(X_train, y_train)
        # print("Best hyperparameters:", grid_search.best_params_)
        RF_pred = rf.predict(X_test)
    
        from sklearn.svm import SVR
        svr = SVR(kernel="rbf")
        svr.fit(X_train, y_train)
        svr_pred = svr.predict(X_test)

        import plotly.graph_objects as go

        fig = go.Figure()
        fig.add_trace(go.Scatter(y=pred,
        
            line_color='rgba(255,0,0,1)',
            
                            mode='lines+markers',
                            name='Linear Regression'))
        fig.add_trace(go.Scatter(y=l, 
                                line_color='rgb(0,176,246)',
                                    
                            mode='lines+markers',
                            name='Decision Tree'))
        fig.add_trace(go.Scatter(y=svr_pred, 
                                line_color='rgb(170,100,20)',
                                    
                            mode='lines+markers',
                            name='SVR'))
        fig.add_trace(go.Scatter(y=RF_pred, 

                                line_color='rgb(180,116,250)',
                                    
                            mode='lines+markers',
                            name='Random Forest'))
        fig.add_trace(go.Scatter(y=y_test, 
                                line_color='rgb(0,255,0)',
                                    
                            mode='lines',
                            name='Actual',
                            line=dict(width=4)))

        fig.update_layout(title=f'{target} prediction using different algorithms',
                        xaxis_title='Values',
                        yaxis_title='Predicted')
        st.plotly_chart(fig,use_container_width=True)
                        

elif selected=='Analytics':
    
    tab1, tabInd, tab2, tab3 = st.tabs(["Regional", "India","EDA", "Performance",])

    d=data.groupby('region')['gdp_per_capita'].mean().sort_values()



    with tab1:

        col1,col2= st.columns(2)

        with col1:
            st.plotly_chart(px.bar(d, x='gdp_per_capita',title="Rankings of Regions based on GDP per capita",orientation='h'),theme='streamlit',use_container_width=True)


        with col2:
            st.plotly_chart(px.scatter(data, x="literacy", y="gdp_per_capita",title='GDP per capita v/s Literacy', size='literacy', color="region",
            hover_name="country", log_x=True),use_container_width=True)
            st.info('__GDP__ of a country is highly dependant upon the __literacy__ and vice versa.')

        
        with col1:
            st.plotly_chart(px.scatter(data, x="agriculture", y="gdp_per_capita", color="region",
                    title='GDP v/s Agriculture (Crops)'),use_container_width=True)
            st.info('Poor countries are more dependant upon harvesting crops than developed countris.')

        with col2:
            st.plotly_chart(px.box(data,x="area",y="gdp_per_capita",points="all"),theme=None,use_container_width=True)
            st.info('As the area increased, the GDP did not kept up.')

        with col1:
            st.plotly_chart(px.bar(data, x='region', y='country'),theme=None,use_container_width=True)
        with col2:
            st.plotly_chart(px.bar(data, x='region', y='gdp_per_capita',color='country',title="GDP of multiple Regions",),use_container_width=True)

    with tab2:
        st.sidebar.markdown('### :orange[For Exploratory Data Analysis]')
        options = st.sidebar.multiselect(
        'Plot your graph by choosing the paremeters',
        ['region', 'gdp_per_capita', 'net_migration', 'phones'],
        ['region', 'gdp_per_capita','net_migration'])
        if len(options)!=3:
            st.warning('Please select only 3.')
            st.stop()
        else:
            st.markdown(f'# The 3D Graph')
            # st.write('You selected:', options)

        st.plotly_chart(px.scatter_3d(data, x=options[0], y=options[1], z=options[2],color=options[0],height=720),use_container_width=True  )
        
        st.plotly_chart(px.scatter_matrix(data, dimensions=data[['population', 'area', 'net_migration', 'gdp_per_capita', 'climate']],width=700, height=720,title="Features relationships",color="gdp_per_capita"),use_container_width=True)

        st.info('You can crop and zoom the graph',icon='ℹ️')
        st.plotly_chart(px.imshow(data.corr(),text_auto=True, aspect="auto"),theme=None,use_container_width=True)

        with st.expander("See Observations"):
            st.write('''
            ### From the above graphs:
        - net_migration & gdp_per_capita has good correlations, which means migrants always prefers to move to the countries having better economy and growth which is gdp in our case.
        - climate and populations are less correlated, means people avoid extreme weather and climate places
        - as area increased the amount of migratants also increased, obvious.
            ''')
            c1,c2 = st.columns(2)
            with c1:
                st.write('''
                - `Strong correlations are`,
                    1. infant_mortality & birthrate
                    2. infant_mortality & literacy
                    3. gdp_per_capita & phones
                    4. arable & other than crops
                    5. birthrate & literacy (less literacy = higher the birthrate)
                ''')
            with c2:
                st.write('''
                - `Weak correlations are`,
                    1. infant_mortality & agriculture
                    2. birthrate & phones
                    3. gdp_per_capita & birthrate
                ''')




    with tab3:
        st.header('Performance Awards 🏆')
        col1, col2, col3 = st.columns(3)
        with col1:

            st.write('''
                1. _`Random Forest` with Feature selection and NO scaling_

                > It did well for Global economy prediction.
                

            - Mean Absolute Error __(MAE)__: 2451.88
            - Root Mean Squared Error __(RMSE)__: 3580.53
            - R-Squared Score __(R2_Score)__: 0.84''')

        with col2:
            st.write('''

        3. _`Linear Regression` with selected features and scaling_
            
            > It did well for Indian economy prediction.
        - Mean Absolute Error __(MAE)__: 2879.521
        - Root Mean Squared Error __(RMSE)__:3756.43
        - R-Squared Score __(R2_Score)__: 0.83''')
        
        with col3:
            st.write('''

        5. _`SVM` with feature scaling and selection_
        - Mean Absolute Error __(MAE)__: 7040.04
        - Root Mean Squared Error __(RMSE)__: 9794.59
        - R-Squared Score __(R2_Score)__: -0.16
        ''')
            
        with col1:
            st.write('''
        2. _`Gradient Boosting` with selected features and scaling_
        - Mean Absolute Error __(MAE)__: 2467.21
        - Root Mean Squared Error __(RMSE)__: 3789.30
        - R-Squared Score __(R2_Score)__: 0.83''')
            
        with col2:

            
            st.write('''

        4. _`Optimised Random Forest`_
        - Mean Absolute Error __(MAE)__: 3564.04
        - Root Mean Squared Error __(RMSE)__: 5915.82
        - R-Squared Score __(R2_Score)__: 0.73''')

    with tabInd:
        import plotly.graph_objects as go

        st.subheader(':orange[Indian] Economy :green[Analysis]')
        # Preprocess
        df=pd.read_csv('India/IndData.csv')
        df = df.rename(columns={'Series Name': 'Year'})
        df['GDP (current US$)'] = df['GDP (current US$)'].astype(float).round(3)
        tmp=df.rename(columns={
        'Population growth (annual %)':'Population',
       'Life expectancy at birth, total (years)':'Lifetime', 
       'GDP growth (annual %)':'GDP', 
       'Inflation, GDP deflator (annual %)':'Inflation',
       'Agriculture, forestry, and fishing, value added (% of GDP)':'AgriForestFish',
       'Industry (including construction), value added (% of GDP)':'Industies',
       'Exports of goods and services (% of GDP)' :'Exports',
       'Imports of goods and services (% of GDP)' :'Imports',
       'Military expenditure (% of GDP)':'MilitaryExp',
        'Merchandise trade (% of GDP)':'MerchandiseTrade',
       'Foreign direct investment, net inflows (BoP, current US$)':'ForeignInvest'

        })
        t=tmp.drop(columns=['Year','Unnamed: 0','MilitaryExp','Population, total', 'Population', 'Lifetime',
       'GDP (current US$)','ForeignInvest','GDP','Inflation'])
        new_df = t.melt(var_name='X', value_name='Value', ignore_index=False)


        col1,col2 = st.columns(2)
        with col1:        
            st.plotly_chart(px.line(df, x="Year", y="GDP growth (annual %)",markers=True,title='Annual GDP growth of India'),use_container_width=True)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['Year'], y=df['Population growth (annual %)'],
                                        fill='toself',
                fillcolor='rgba(231,107,243,0.7)',
                line_color='rgba(255,0,0,1)',
                
                                mode='lines+markers',
                                name='Population growth'))
            fig.add_trace(go.Scatter(x=df['Year'], y=df['Life expectancy at birth, total (years)'],
                                    line_color='rgb(0,176,246)',
                                        fill='toself',
                fillcolor='rgba(31,50,243,0.2)',
                                mode='lines+markers',
                                name='Life expectancy'))
            fig.update_layout(title='Life expectancy(Age) and Population growth (%)',
                            xaxis_title='Year',
                            yaxis_title='Life expectancy and Population growth')
            st.plotly_chart(fig,use_container_width=True)


            fig = px.bar(new_df['X'],x='X',y=new_df['Value'],  text_auto='.2s',
                        color=new_df['X'],
                        height=500,
                        width=900,
                        title="% Contribution for GDP by different sectors")
            fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
            st.plotly_chart(fig,use_container_width=True)


        with col2:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['Year'], y=df['Imports of goods and services (% of GDP)'], name='Imports',
                         line=dict(color='firebrick', width=4,
                              dash='dashdot') # dash options include 'dash', 'dot', and 'dashdot'
            ))
            fig.add_trace(go.Scatter(x=df['Year'], y=df['Exports of goods and services (% of GDP)'], name='Exports',
                                    line=dict(color='royalblue', width=4, dash='dot')))

            fig.update_layout(title='Import and Export of goods and services (% of GDP)',
                            xaxis_title='Year',
                            yaxis_title='Exports/Import of goods and services (% of GDP)')
            
            st.plotly_chart(fig,use_container_width=True)

            fig = px.line(df,x='Year',y='Population, total',
            markers=True,
            title="Total Population of India annually")
            fig.update_traces(textfont_size=12,cliponaxis=False)
            st.plotly_chart(fig,use_container_width=True)

            fig = px.bar(tmp,x='Year',y='ForeignInvest',  text_auto='.1s',

            title="Year by year Foreign investments of India")
            fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
            st.plotly_chart(fig,use_container_width=True)



        with st.expander("See Observations",expanded=True):
            st.write('''
            ### From the above graphs:
        -   The GDP growth of India has been declining since 2016, and hit lowest in 2020.
        -   Our import business is always higher than export, which can't be good always for our economical independance.
        -   As the decades unfolded, population of India decreased, although life expectancy kept increasing.
        -   Industries and Merchandise Trading are the two leaders to contributing GDP growth of India.
        -   Foreign investments are exponentially increasing as the years progressed, which is a very healthy sign for our economy.
            ''')

            


elif selected == 'Help':
    with st.container():

        st.write('''
        The :blue[**Gross Domestic Product**] (GDP) is one of the metrics to ensure self-sustained growth for any country. 
        The total monetary value of goods and services flowing through an economy over time is measured by GDP. 
        ''')

        st.write('''
        ### The goal of our project _Generic GDP Prediction and Analysis_ to find the **:red[Patterns]** inside the taken dataset of multiple countries, and to make the **:blue[Prediction]** using Supervized Machine Learning algorithm. This project ivolves applications of :orange[Data Analysis], :violet[Prediction] and :green[Recommendation] using Machine Learning.    
        ''')
        with st.expander('See more about Global dataset'):
            st.markdown('''
            `It has 20 columns and 227 rows (countries)`

            `Area`: sq.mi 

            `Population` density: per sq.mi 

            `Coastline`: coast/area ratio

            `Infant mortality`: per 1000 births

            `GDP`: $ per capita

            `Phones`: per 1000    

            `Literacy,Arable,Crops,Other`: percentages (%)


            ''')


        st.write('''
        # Takeaways from this project:

            1. Basic authentication system.
            2. Data prediction based on given values.
            3. Data visualization by the interactive and 3D graphs.
            4. Comparative analysis of multiple supervised algorithms.
            5. Getting recommended values to improve the GDP of selected country.
            6. Some important realizations of relationships between multiple features.
            7. Indian economy analysis and prediction of any feature. 

        
        ''')

        st.markdown('''
        > :blue[Source:] All these data sets taken up from the US government and World Bank open data.
        ### What inspired us to do this project?

            Understanding of economy and growth of all countries is an essential for all citizens.
            As we are progressing towards machine learning and artificial intelligence era, it is helping us to
            understand complex problems having good amount of data. 
            
            The data analysis and engineering is very essential and critical in modern day world. 
            Data science can provide excellent insight of data using patterns, trends and relationship between 
            multiple parameters,  which would be impossible for any human being to manually calculate them by having 
            data in rows and columnar fashion.  

            This process of understanding GDP of any country's and providing options to change parameters to predict its future
            value became very interesting topic for us. We want to provide some suggestions such as area, sectors to improve any
            country's GDP per capita.                    
                    ''')

        st.write('''
        ### Methodology
        
        :blue[Step 1]. Identifying the :red[research goal] that our project aims and context to deliver and measure of success.
        
        :blue[Step 2]: Data can be stored in a :red[variety of formats], from plain text files to database tables. The objective now is to acquire the related data. Realize the importance and sensitivity of data, and often have norms in place to ensure that everyone has access to just what they want.
        
        :blue[Step 3]: Data Cleansing integrating, and transforming data are the main steps in :red[data preparation].  However, the clean and validated information is gathered from open source. The dataset is clean and hence can be used as it is
        
        :blue[Step 4]: This stage focuses on :red[data exploration].  Extra Trees Regressor class is used to implement a Meta estimator that fits several decision trees on various sub samples. We are also using Plotly visual analysis tool for detailed data exploration.
        
        :blue[Step 5]: Model is designed with clean data and a :red[clear understanding of the content] in order to make better predictions, identify objects, or gain an understanding of the system to model.

        ''')

        st.write('''
        ### Validation 
            - The datapoints are near to actual values with the limited data that we have
            - Altough there are slight dissimilarities, did not ruin our analysis
            - Values are bit OLD, not updated to this date. (population, areas, phones etc.)
                 ''')
        






        st.markdown(f":red[©️ Vilas Hegde - {date.today().year}]")
elif selected=='Recommendation':
    tab1,tab2 = st.tabs(["Global", "India"])
    df = pd.read_csv('./India/IndData.csv')
    df=df.drop(columns=['Unnamed: 0'])
    with tab1:
        country = st.selectbox(
        'Choose a country',
        data.country.unique()
        )
        correlation_matrix = data.corr()['gdp_per_capita']

        corr_values_sorted = correlation_matrix.sort_values(ascending=False)

        # st.write(corr_values_sorted)
        # st.stop()
        # st.table(corr_values_sorted)
        # st.plotly_chart(px.imshow(correlation_matrix,
        #             labels=dict(x="Columns", y="Columns", color="Correlation"),
        #             x=correlation_matrix.columns,
        #             y=correlation_matrix.columns,
        #             color_continuous_scale='RdBu',
        #             zmin=-1,
        #             zmax=1))
        selected_features = corr_values_sorted[(corr_values_sorted >= 0.5) | (corr_values_sorted <= -0.5)].index.tolist()

        # st.write(selected_features)



        selected_data_table=data[selected_features[1:]].loc[data.country==country]
        selected_data_table = selected_data_table.rename(index={0: country})
        # Rename the index and give it a name
        selected_data_table= selected_data_table.rename_axis('Country').reset_index()
        selected_data_table['Country']=country
        gdp=data.gdp_per_capita[data['country']==country]

        target_value = st.slider(f"Your expectation to reach GDP of {country}", min_value=float(gdp), max_value=99999.0, value=None, step=1.0, format=None, key=None, help='You predict the GDP, and we will recommend the ways to get to there.', on_change=None, args=None, kwargs=None,disabled=False, label_visibility="visible")
        
        if (target_value > float(gdp)):
            percentage_increase = ((target_value - float(gdp)) / float(gdp)) * 100
            st.write(f'''
                    `{int(percentage_increase)}% increase`
                    ''')
            col1,col2=st.columns(2)
            with col1:
                st.metric(label=f"GDP in 2006",value=gdp,delta=float(gdp)-target_value)
            with col2:
                st.metric(label=f"Expectated GDP",value=target_value,delta=target_value - float(gdp))


            selected_data_table.columns = ['Country','Phones/capita','Service',	'Literacy',	'Agriculture',	'Infant_mortality',	'Birthrate']
            # Display the DataFrame in a Streamlit table
            st.subheader('Data that are in our dataset:')
            st.write(selected_data_table.to_html(index=False), unsafe_allow_html=True)

            


            with st.expander('Recommended results',expanded=True):
                col1,col2= st.columns(2)
                with col1:
                    improve={'Phones':selected_data_table['Phones/capita'][0],
                            'Service':selected_data_table['Service'][0],
                            'Literacy':selected_data_table['Literacy'][0]}
                    # st.json(improve)
                    for i,val in improve.items():
                        improve[i] = val * (1 + (int(percentage_increase) / 100))
                        # st.write(i,val)
                    # st.json(improve,expanded=False)
                    st.header(':green[Improve] :arrow_up:')
                    for i,val in improve.items():
                        st.subheader(f"{i} by :green[{val.round(2)}] units")
                        # st.write(i,val)

                with col2:
                    decrease={'Birthrate':selected_data_table['Birthrate'][0],
                            'Infant Mortality':selected_data_table['Infant_mortality'][0],
                            'Agriculture':selected_data_table['Agriculture'][0]}
                    # st.json(decrease)
                    for i,val in decrease.items():
                        decrease[i] = val * (1 + (int(-percentage_increase) / 100))
                        # st.write(i,val)
                    # st.json(decrease,expanded=False)

                    st.header(':orange[Decrease] :arrow_down:')
                    for i,val in decrease.items():
                        st.subheader(f"{i} by :red[{val.round(2)}] units")
        with st.expander('View impactness of features',expanded=False):
            col1,col2= st.columns(2)
            with col1:
                st.header('High positive impact')
                st.info('These are directly proportional to GDP', icon="📈")

                for i in selected_features[1:4]:
                    st.success('__'+i.capitalize()+'__')
                

            with col2:
                st.header('High negative impact')
                st.info('These are inversely proportional to GDP', icon="📉")
                for i in selected_features[-1:-4:-1]:
                    st.error('__'+i.capitalize()+'__')

    with tab2:
        # df=df.drop(columns=['Unnamed: 0'])
        # st.table(df.head())
        correlation_matrix = df.corr()['GDP (current US$)']
        # correlation_matrix=correlation_matrix.drop(columns=['Unnamed: 0'])
        corr_values_sorted = correlation_matrix.sort_values(ascending=False)

        selected_features = corr_values_sorted[(corr_values_sorted >= 0.5) | (corr_values_sorted <= -0.5)].index.tolist()
        selected_features.remove('Year')
        selected_data_table=df[selected_features[1:]].loc[df['Year']==2020]
        # selected_data_table=selected_data_table.drop(columns=['Unnamed: 0'])
        gdp=df['GDP (current US$)'][df['Year']==2020]
        gdp=float(gdp)
        if gdp >= 1000000000:
            gdp= str(gdp/1000000000)[:4] + ' B.'
        elif gdp >= 1000000:
            gdp= str(gdp/1000000)[:4] + ' M.'
        st.sidebar.metric(value=gdp,label="India's GDP in 2020")

        target_value= st.slider('How much GDP you want India to reach?',min_value=float(gdp[:3]),max_value=10.0,step=.5)
        if (target_value > float(gdp[:3])):
                    percentage_increase = ((target_value - float(gdp[:3])) / float(gdp[:3])) * 100
                    st.write(f'''
                            `{int(percentage_increase)}% increase`
                            ''')
                    col1,col2=st.columns(2)
                    with col1:
                        st.metric(label=f"GDP in 2020",value=gdp,delta=float(gdp[:3])-target_value)
                    with col2:
                        st.metric(label=f"Expectated GDP",value=str(target_value)+' B.',delta=target_value - float(gdp[:3]))

                    st.subheader('Data that are in our dataset:')
                    st.write(selected_data_table.to_html(index=False), unsafe_allow_html=True)
                    
                    
                    with st.expander('Recommended results',expanded=True):
                        col1,col2= st.columns(2)
                        # st.table(selected_data_table)
                        with col1:  
                            improve={'Life expectancy at birth, total (years)':float(selected_data_table['Life expectancy at birth, total (years)']),
                                    'Population, total':float(selected_data_table['Population, total']),
                                    'Merchandise trade (% of GDP)':float(selected_data_table['Merchandise trade (% of GDP)']),
                                    'Foreign direct investment, net inflows (BoP, current US$)':float(selected_data_table['Foreign direct investment, net inflows (BoP, current US$)']),
                                    'Imports of goods and services (% of GDP)':float(selected_data_table['Imports of goods and services (% of GDP)']),
                                    'Exports of goods and services (% of GDP)':float(selected_data_table['Exports of goods and services (% of GDP)']),
                                    'Agriculture, forestry, and fishing, value added (% of GDP)':float(selected_data_table['Agriculture, forestry, and fishing, value added (% of GDP)'])
                            }
                        #     # st.json(improve)
                            for i,val in improve.items():
                                if val >= 1000000000:
                                    val = val * (1 + (int(percentage_increase) / 100))
                                    val= str(val/1000000000)[:4] + ' B.'
                                    improve[i]=val
                                else:
                                    improve[i] = val * (1 + (int(percentage_increase) / 100))
                                # st.write(i,val)
                            # st.json(improve,expanded=False)
                            st.header(':green[Improve] :arrow_up:')
                            for i,val in improve.items():
                                st.subheader(f"{i} by :green[{val}] units")
                                # st.write(i,val)

                        with col2:
                            decrease={'Population growth (annual %)':float(selected_data_table['Population growth (annual %)']),
                                    'Agriculture, forestry, and fishing, value added (% of GDP)':float(selected_data_table['Agriculture, forestry, and fishing, value added (% of GDP)']),
                                    
                                    }
                            # st.json(decrease)
                            for i,val in decrease.items():
                                val = val * (1 + (int(-percentage_increase) / 100))
                                decrease[i] = abs(val)
                                # st.write(i,val)
                            # st.json(decrease,expanded=False)

                            st.header(':orange[Decrease] :arrow_down:')
                            for i,val in decrease.items():
                                st.subheader(f"{i} by :red[{str(val)[:4]}] %")
        with st.expander('View impactness of features',expanded=False):
                            col1,col2= st.columns(2)
                            # st.table(corr_values_sorted)
                            with col1:
                                st.header('High positive impact')
                                st.info('These are directly proportional to GDP', icon="📈")

                                for i in selected_features[1:8]:
                                    st.success('__'+i.capitalize()+'__')
                                

                            with col2:
                                st.header('High negative impact')
                                st.info('These are inversely proportional to GDP', icon="📉")
                                for i in selected_features[-1:-3:-1]:
                                    st.error('__'+i.capitalize()+'__')