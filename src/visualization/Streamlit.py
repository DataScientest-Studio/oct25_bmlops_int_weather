import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

import pickle

###***************************************************************************************************************
#### Title & page architecture
st.title("Rain in Austrailia")
st.sidebar.title("Table of Contents")

pages = ["Introduction", "Data-set :date:", "Automation", 
         "Modelling :chart_with_downwards_trend:", 
         'Prediction :chart_with_upwards_trend:', 'Conclusion:grey_exclamation:']
page = st.sidebar.radio("Go to:", pages)

###**************************************************************************************************************
### Page 1: Introduction

if page == pages[0]:
    st.subheader("Introduction")

###**************************************************************************************************************
### Page 2: Dataset

if page == pages[1]:
    st.subheader("Dataset")

###**************************************************************************************************************
### Page 3: Automation

if page == pages[2]:
    st.subheader("Automation")

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
    st.subheader("Conclusion")