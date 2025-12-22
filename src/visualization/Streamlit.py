import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from graphviz import Digraph

from sqlalchemy import create_engine
import pickle
###***************************************************************************************************************

engine = create_engine(r'sqlite:///C:\Users\stefa\Documents\GitHub\oct25_bmlops_int_weather\data\raw\weather_australia.db')

# SQL-Query oder Tabellennamen
query = "SELECT * FROM weather_table"

# In DataFrame laden
df = pd.read_sql(query, engine)


###***************************************************************************************************************
#### Title & page architecture
st.title("Rain in Australia :partly_sunny:")
st.sidebar.title("Table of Contents")

pages = ["Introduction", "Data-set :date:", "Automation", 
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


###**************************************************************************************************************
### Page 2: Dataset

if page == pages[1]:
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

    #group_hybrids=df.groupby(['RainToday']).agg({'RainTomorrow': ['value_counts']})
    #st.write(group_hybrids)

    st.subheader("Preprocessing Steps")

    if st.checkbox(" **Show missing values**"):
        st.write('Missing values in %')
        st.dataframe(np.round(df.isna().sum()/len(df)*100).sort_values(ascending=False),width=200)

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


    cats = df.Location.unique()
    cat_choice = st.selectbox("Select a Location:", cats)

    if cat_choice:
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.countplot(data=df[df['Location']==cat_choice], x='RainToday', hue='RainTomorrow', ax=ax)
        ax.set_title(f"Distribution of {cat_choice}")
        st.pyplot(fig)

###**************************************************************************************************************
### Page 3: Automation

if page == pages[2]:
    st.subheader("Automation")

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

###**************************************************************************************************************
### Page 4: Modelling

if page == pages[3]:
    st.subheader("Modelling")


###**************************************************************************************************************
### Page 5: Prediction

if page == pages[4]:
    st.subheader("Prediction")


###**************************************************************************************************************
### Page 6: Conclusion

if page == pages[5]:
    st.subheader("Conclusion and Outlook")
