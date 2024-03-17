import sqlite3
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd #pip install pandas
from fastapi import FastAPI # Import FastAPI:.
from fastapi import HTTPException
from fastapi.responses import Response
from datetime import datetime

app88 = FastAPI()# create an instance of the FastAPI class

@app88.get("/") #decorator provided by FastAPI
def read_root():#function for GET request  
    return {"Status": "alive! "}

@app88.get("/dbg") #decorator provided by FastAPI
def read_debag():#function for GET request  
    r = os.getcwd()
    return r

# === VINES 
@app88.get("/wine_finder/{wine}")
def read_item_list(wine: str):      
    # read sql
    with open(r"../_sqlapi/Query08api1.sql", "r") as file: 
        sql = file.read() 
    # put variable to sql
    wine ="'%"+ wine[1:-1] +"%'" # preparation of variable  
    sql = sql.replace('@VINE', wine ) # preparation of sql
    # connect to db
    conn = sqlite3.connect(r"../wine.db")
    # put response to text variable
    w0,r = 0,""
    r = r"<strong>THE LIST OF FOUND WINES:</strong>" + "\n"
    r+= r'<em> This is a wine search page for further the search of analogs at https://api-wines1.onrender.com/wine_analogue_finder/""' + "\n"
    r+= r" To find the wine you are interested in, enter part of its name at the end of the web-address to this page in double quotes"+ "\n"
    r+= r'EXAMPLE:: link for "Cabernet Sauvignon" wine ==> https://api-wines1.onrender.com/wine_finder/"Cabernet%Sauvignon"' + "\n"
    r+= r'If the name of the wine contains several words, put a "%" sign between them.' + "\n"
    r+= r'If you want to see all varieties, just put the % sign between the quotes'
    r+="</em>"+"\n"+"----------------------------------------------------------------------\n"
    x=1
    for row in conn.cursor().execute(sql):
        r += str(x)+". "+ row[0] + ", price=" + str(row[1]) + "euro \n" 
        x+=1
    r += "-------------------------------------------------\n search string " + wine   
    r += str(datetime.now())[:19] + "\n" 
    r = r.replace('\n', '<br>').replace(' ', '&nbsp;').replace('\n', '<br>')
    r = Response(content= r, media_type="text/html")  
    return r 

# === ANALOGS 
@app88.get("/wine_analogue_finder/{wine}")
def read_item_finder(wine: str):#, q: Union[str, None] = None):
    # read sql
    with open(r"../_sqlapi/Query08api2.sql", "r") as file: sql = file.read()
    wine = wine.replace(' ','%')
    sql=sql.replace('@VINE',"" + wine + "")
    # connect to db
    conn = sqlite3.connect(r"../wine.db") 
    # put response to text variable
    w0,r = 0,""    
    r+= r"<strong>THE LIST OF ALTERNATIVES FOR FOUND WINES (5 for each):</strong>" + "\n"
    r+= r"<em>Wine varieties matching your search are marked in bold." + "\n"
    r+= r"Alternatives with similar taste, rating, and price are shown in regular font"+ "\n"
    r+= r"Alternatives with a greater number of Taste Confirmations by Consumers (TCC) are shown first"+"\n"
    r+= r'At first you have to find certain wine here: https://api-wines1.onrender.com/wine_finder/"caberne"' + "\n"
    r+= r'The selected wine must then be enclosed in double quotes at the end of the link to this page.' + "\n"
    r+= r'EXAMPLE:: link for "Cabernet Sauvignon" wine ==> https://api-wines1.onrender.com/wine_analogue_finder/"Cabernet Sauvignon"' + "\n"

    r+= "</em>"
    r+= r"-----------------------------------------------------------------------------------------"
    x=1
    for row in conn.cursor().execute(sql): 
        ## print(x,row[1])
        w1,ww,cc = row[1],row[4],str(row[6])
        if w0==0 or w1!=w0:           
            r += "\n" + '<strong>' + str(x) +". " + w1  + '</strong>' + "/TCC=" + cc # main: set as font bold      
            r += "\n" + '  ' + ww + " / TCC=" + cc # analog
            x+=1
        else: 
            if w1==w0: r += '  ' + ww + " / TCC=" + cc # analog
        w0 = w1 
        r += "\n"                

    r += "-------------------------------------------------\n search string " + wine
    r += str(datetime.now())[:19] + "\n"  
    r = r.replace('\n', '<br>').replace(' ', '&nbsp;').replace('\n', '<br>')   
    r = Response(content= r, media_type="text/html")
    return r 
        

# x=read_item("caberne")