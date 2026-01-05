import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from graphviz import Digraph
import requests
from sqlalchemy import create_engine
import os

###***************************************************************************************************************

# read data from the sql container
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_HOST = "weather_sql_container"  # Network? eg my_network
MYSQL_PORT = 3306
MYSQL_DB = "weather_db"
TABLE_NAME = 'weather_data'
engine = create_engine(
         f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
         )

# SQL-Query oder Tabellennamen
query = f"SELECT * FROM {TABLE_NAME}"

# In DataFrame laden
df = pd.read_sql(query, engine)


###***************************************************************************************************************
#### Title & page architecture
st.title("Rain in Australia :partly_sunny:")
st.sidebar.title("Table of Contents")

pages = ["Introduction", "Automation", "Preprocessing :date:",
         "Modelling :chart_with_downwards_trend:", 
         'Prediction :chart_with_upwards_trend:', 'Conclusion:grey_exclamation:']
page = st.sidebar.radio("Go to:", pages)

###*************************************************************************************************************

###**************************************************************************************************************
### Page 1: Introduction

if page == pages[0]:
    st.subheader("Introduction :cloud_with_rain:")

    st.write('The future weather is an important information for lots of areas of life e.g. agriculture or leisure activities')
    st.write('The aim of the project is to predict if it is raining tomorrow based on today weather.')

    st.subheader("Dataset")
    st.write('The given Dataset from Australia has', df.shape[1] ,'different columns and contains ', df.shape[0] ,' data entrys. ' \
    'The target column is RainTomorrow, which is a Boolean. ' )
    st.dataframe(df)

    st.write(
    'The Data for today contains information about the date, the city, temperature, humidity, pressure, wind, clouds, ' \
    'sunshine and rain. Most variables are numeric. Categorical values are the location and wind related values '
    '(e.g. wind direction). Rains today is a boolean. The dataset contains measurements from 49 citys/places.')

    st.subheader("First observations")
    st.write('The target is unevenly distibuted (fewer rainy days). ')

    fig, ax = plt.subplots()
    sns.countplot(data=df, x='RainTomorrow')
    plt.title('Rain Tomorrow')
    plt.xticks(rotation=45)
    plt.xlabel('')
    st.pyplot(fig);

    st.write('If it rains today, there is 50% chance that it also rains tomorrow. If it does not rain today, ' \
    'it will most likely also not rain tomorrow.')


    fig, ax = plt.subplots()
    sns.countplot(data=df, x='RainToday', hue='RainTomorrow')
    plt.title("Countplot RainTomorrow grouped by RainToday")
    st.pyplot(fig);


    if st.checkbox(" **Show missing values**"):
        st.write('Missing values in %')
        st.dataframe(np.round(df.isna().sum()/len(df)*100).sort_values(ascending=False),width=200)

    
    cats = df.Location.unique()
    cat_choice = st.selectbox("Select a Location:", cats)

    if cat_choice:
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.countplot(data=df[df['Location']==cat_choice], x='RainToday', hue='RainTomorrow', ax=ax)
        ax.set_title(f"Distribution of {cat_choice}")
        st.pyplot(fig)


###**************************************************************************************************************
### Page 2: Automation

if page == pages[1]:
    st.subheader("Project Structure")

    dot = Digraph()
 
# Knoten hinzufügen

    dot.node("A","Database (SQL)",style="filled",fillcolor="lightblue", color='blue')
    dot.node("B", "Preprocessing",style="filled",fillcolor="lightblue", color='blue')
    dot.node("D", "Modell Training and Prediction",style="filled",fillcolor="lightblue", color='blue')
    dot.node("E", "MLFlow",style="filled",fillcolor="lightblue", color='blue')
    dot.node("F", "API",style="filled",fillcolor="lightblue", color='blue')
    dot.node("G", "Streamlit",style="filled",fillcolor="lightblue", color='blue')

# Kanten hinzufügen (Verbindungen)
    dot.edge("A", "B", label="")
    dot.edge("B", "A", label="")
    dot.edge("D", "A", label="")
    dot.edge("A", "D", label="")
    dot.edge("E", "D", label="")
    dot.edge("D", "E", label="")
    dot.edge("F", "D", label="")
    dot.edge("D", "F", label="")
    dot.edge("G", "F", label="")
    dot.edge("F", "G", label="")
    dot.edge("A", "G", label="")

# Diagramm in Streamlit anzeigen
    st.graphviz_chart(dot)


    st.subheader("Dockerisation")
    st.write( 
    'four docker containers: mysql, MLFlow, Streamlit and model services \n' \
    '- mysql container hosts all the raw data \n' \
    '- MLFlow container hosts the mlflow server for storing and restoring the best models\n' \
    '- model container hosts the data substracting, data preprocessing, training, predicting, and FastAPI services\n' \
    '- Streamlit container hosts the Streamlit app\n'' \n' \
    '- to start(or build if not exists) the docker compose use docker compose up and docker-compose.yml - file\n' \
    '- to open the Streamlit app, in your browser, go to http://localhost:8501/\n'\
    '- to visit the MLflow server, in your browser, go to http://localhost:8080/\n')

    st.subheader("Automation")
    st.write( 
    'using crontab to automate process: \n' \
    '- make dataset (chooses a random part of the original data to simulate changes in the data) \n' \
    '- preprocess data\n' \
    '- train model\n' \
    '- predict with best model\n')

###**************************************************************************************************************
### Page 3: Preprocessing

if page == pages[2]:
    
    st.subheader("Preprocessing Steps")

    st.write( 
    '- delete features with over 10% of missing values \n' \
    '- replace Nans for categorical variables with mode \n' \
    '- replace Nans for numerical variables with median\n' \
    '- delete Date column since it is not used for modelling (note: The date is deleted for making the model easier. ' \
    'One should keep in mind that the seasons in fact have an influence on the weather. Therefore for'\
    ' advanced modelling the date/month should be considered)\n' \
    '- encode RainToday and RainTomorrow in binary variable \n' \
    '- encode location and variables for wind direction with get_dummies (note: Since there are a lot of Locations in the'\
    ' dataset, this step leads to an enormous increase of the number of features\n' \
    '- Scaling of numerical features by vector normalization\n')


    st.write('Pressing the button "Make dataset" randomly chooses 20% of the original data to create a new dataset')
    if st.button("Make dataset"):
        MODEL_API = os.getenv("MODEL_URI")
        if MODEL_API is not None:
            response = requests.get(f"{MODEL_API}/make_dataset")
            if response.status_code == 200:
                st.success("Sub-dataset created!")
            else:
                st.error("Failed to create sub-dataset.")

    st.write('Pressing the button "Preprocess" preprocesses the newest dataset')
    if st.button("Preprocess"):
        MODEL_API = os.getenv("MODEL_URI")
        if MODEL_API is not None:
            response = requests.get(f"{MODEL_API}/preprocessing")
            if response.status_code == 200:
                st.success("Preprocessing done!")
            else:
                st.error("Failed to preprocess.")
    
###**************************************************************************************************************
### Page 4: Modelling

if page == pages[3]:
    st.subheader("Modelling")
    st.write('The modelling script does model 4 different modeltypes:\n' \
    '- KNeighbors\n' \
    '- Decision Tree\n' \
    '- Random Forest\n' \
    '- Gradient Boosting\n')

    st.write('The modeling script then stores the best model with MLFlow.')

    st.write('Pressing the button "Train model" starts the training process with the newest dataset')
    if st.button("Train model"):
        MODEL_API = os.getenv("MODEL_URI")
        if MODEL_API is not None:
            response = requests.get(f"{MODEL_API}/training")
            if response.status_code == 200:
                st.success("Start to train Model!")
            else:
                st.error("Failed to train model.")


###**************************************************************************************************************
### Page 5: Prediction

if page == pages[4]:
    st.subheader("Prediction")

    st.write('The prediction script uses the best model stored in the previous step with MLFlow.')

    st.write('Pressing the button "Predict" starts the prediction process with the newest dataset')
    if st.button("Predict"):
        MODEL_API = os.getenv("MODEL_URI")
        if MODEL_API is not None:
            response = requests.get(f"{MODEL_API}/predict")
            if response.status_code == 200:
                st.success("Start to predict!")
            else:
                st.error("Failed to predict.")


###**************************************************************************************************************
### Page 6: Conclusion

if page == pages[5]:
    st.subheader("Conclusion")

    st.write('- The project does predict the weather of tomorrow by using changing data automaticly\n' \
    '- The steps for the modelling and prediction are automized by crontab\n' \
    '- For the application 5 Docker containers are used. Communicating between each other\n' \
    '- Since the focus of the project is to use machine engineering tools, the model performances are not that good')

    st.subheader("Outlook")

    st.write('If we had more time for the project we would have tried:\n' \
    '- 1) Automatisation using Airflow instead of cron\n' \
    '- Advantages of Airflow: better monitoring of the models, more complex workflows possible\n' \
    '- 2) Data version control using DagsHub\n' \
    '- Advantages of DagsHub: better tracking of data changes over time, necessary for frequently updated data\n' \
    '- 3) Create one docker container for each single task (e.g. one for preprocessing, one for training etc.)\n' \
    '- Advantages: better scalability and maintainability of the project\n' \
    '- 4) Adding more functioniality to the streamlit app (e.g. visualizations of model performances, feature selection in the preprocessing)')

