import sqlite3
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd #pip install pandas
from fastapi import FastAPI 
# from fastapi import HTMLResponse
from fastapi.responses import Response
from datetime import datetime
from fastapi.staticfiles import StaticFiles


app88 = FastAPI() # create an instance of the FastAPI class

# Mount the /static/ directory to serve static files
app88.mount("/_static", StaticFiles(directory="_static"), name="_static")

@app88.get("/") #decorator provided by FastAPI
def read_root():#function for GET request  
    return {"Status": "alive! "}

@app88.get("/dbg") #decorator provided by FastAPI
def read_debag():#function for GET request  
    r = os.getcwd()
    return r

def process_vintage(row):
    aa = row['vintage'].split(',')
    a5 = ', '.join((aa[:5]))
    if len(aa) > 5:
        b = a5 + ' and ' + str(len(aa) - 5) + ' more'
    else:
        b = a5
    return b

@app88.get("/w_list")
def wlist():      
    # read sql
    with open(r"./_sqlapi/Query08api01.sql", "r") as file: sql = file.read() 
    conn = sqlite3.connect(r"./wine.db") 
    if os.path.exists('Dockerfile'):
       url = 'http://127.0.0.1:8000/substitutes/'
    else:
       url = 'https://zero2-sommelier.onrender.com/substitutes/'

    df = pd.read_sql_query(sql, conn)
    df['vintage'] = df.apply(process_vintage, axis=1)    
    df['name&click']= f'<a href="{url}' + df['id'].astype(str) +'">'+ df['name']+'</a> '    
    df_sub = df[['rn','id', 'name&click', 'winery_id', 'price1L', 'rating',  'vintage']]    
    df_subhtml = df_sub.to_html(index = False, escape=False ) #escape - to save links
    df_subhtml = df_subhtml.replace('<table border="1" class="dataframe">','')
    df_subhtml = df_subhtml.replace('</table>','')

    html_text = f"""
    <head>
        <link rel="stylesheet" href="/_static/styles.css" >
        <div class='style1'>  {str(datetime.now())[:19]} </div>       
        <div class='style2'>  THE LIST OF WINES  </div><br>     
        <div class='style1'>
            This is a list of the various wines in stock.<br>
            Click on the name of a wine to see the most popular alternatives carefully selected based on taste, price and rating. 
    </head>
    <body>        
        <table class='styled-table2'>{df_subhtml}</table><br>        
        <div class='style1'>  EXPLANATION: </div>   
        <div class='style1'>  <strong> id </strong> - indicates the order number of wine in the list </div>   
        <div class='style1'>  <strong> winery_id </strong> - indicates the order number of wineries in the list. Used to differentiate between various     types of wine with the same name from different wineries. </div>   
        <div class='style1'> <strong> taste index </strong> - an integrated measure indicating the total number of flavor nuances confirmed by users that match between the original and substitute. <br>It also considers the type of taste - primary (weighted 100%) and secondary (weighted 50%). </div>   
        <div class='style1'>  <strong> price1L </strong> - price for 1 liter in euro. </div>   
        <div class='style1'>  <strong> rating </strong> - average user rating </div>   
        <div class='style1'>  <strong> vintage </strong> - vintage years for this wine </div>  
    </body>
""" 
    # open(r"./html_sub.html", "w", encoding="utf-8").write(df_subhtml) # for debug
    return Response(content= html_text, media_type="text/html")

@app88.get("/substitutes/{wine}")
def read_item_finder(wine: str):#, q: Union[str, None] = None):
    # read sql
    with open(r"./_sqlapi/Query08api02.sql", "r") as file: sql = file.read()
    wine = wine.replace(' ','%')
    sql=sql.replace('@VINE',"" + wine + "")
    conn = sqlite3.connect(r"./wine.db") 
    df = pd.read_sql_query(sql, conn)  
    df_sub = df[['type2','id2','name2', 'winery_id2', 'taste_index', 'price1L2', 'rating2',  'vintage']]
    df_sub = df_sub.rename(columns = lambda x: x.replace('2', ''))
    df_subhtml = df_sub.to_html( escape=False)#escape - to save links
    df_subhtml = df_subhtml.replace('<table border="1" class="dataframe">','')
    df_subhtml = df_subhtml.replace('</table>','')

    html_text = f"""
    <head>
        <link rel="stylesheet" href="/_static/styles.css" >
        <div class='style1'>  {str(datetime.now())[:19]} </div>
        <div class='style1'>  You've selected the vine  </div>
        <div class='style2'>   {df.iloc[0]['name'].upper()} </div>
        <div class='style3'> id {df.iloc[0]['id']} </div><br>
        <div class='style3'>
            The table for selecting alternatives with the closest wines based on taste, rating, and price</div>        
    </head>
    <body>        
        <table class='styled-table2'>{df_subhtml}</table><br>        
        <div class='style1'>  EXPLANATION: </div>   
        <div class='style1'>  <strong> id </strong> - indicates the order number of wine in the list </div>   
        <div class='style1'>  <strong> winery_id </strong> - indicates the order number of wineries in the list. Used to differentiate between various     types of wine with the same name from different wineries. </div>   
        <div class='style1'> <strong> taste index </strong> - an integrated measure indicating the total number of flavor nuances confirmed by users that match between the original and substitute. <br>It also considers the type of taste - primary (weighted 100%) and secondary (weighted 50%). </div>   
        <div class='style1'>  <strong> price1L </strong> - price for 1 liter in euro. </div>   
        <div class='style1'>  <strong> rating </strong> - average user rating </div>   
        <div class='style1'>  <strong> vintage </strong> - vintage years for this wine </div>  
    </body>
"""  
    conn.close()
    return Response(content= html_text, media_type="text/html")
        

