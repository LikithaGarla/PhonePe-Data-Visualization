import pandas as pd
import streamlit as st 
import numpy as np
from PIL import Image
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import psycopg2
import os
import git
from git import Repo

st.title('Phone pe data visualisation')
st.sidebar.title("Selector")

con = psycopg2.connect(
        database="likitha",
        user="postgres",
        password="likitha25",
        host="localhost",
        port= '5432'
        )

cursor_obj = con.cursor()
cursor_obj.execute("SELECT * FROM PhonePeCountry")
values = cursor_obj.fetchall()

df = pd.DataFrame(values, columns = ['state', 'count', 'amount'])
#st.write(df)
visualisation = st.sidebar.selectbox('Select Chart type',('Bar Chart','Pie Chart'))
if(visualisation == 'Bar Chart'):
    graph = px.bar(df,x='state',y='count')
    st.plotly_chart(graph)
elif visualisation == 'Pie Chart':
    fig=px.pie(df,values=df['count'],names=df['state'])
    st.plotly_chart(fig)

def InsertintoDatabase():
    data1 = json.load(json_file)
    for i in data1['data']['hoverDataList']:
        name = i['name']
        count = i['metric'][0]['count']
        amount = i['metric'][0]['amount']
    #print(name,count,amount)
    try:
        cursor_obj.execute("INSERT INTO PhonePeCountry VALUES(%s,%s,%s)", (name,count,amount))
        con.commit()
        print('working')
    except:
        print('Not working')
        con.rollback()

def ConnectwithGit():
    os.environ["GIT_PYTHON_REFRESH"] = "quiet"
    Repo.clone_from('https://github.com/PhonePe/pulse.git','E:/DataSciencePrograms/PhonePeGitRepo')
