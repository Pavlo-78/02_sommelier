import sqlite3
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd #pip install pandas
from fastapi import FastAPI 
# from fastapi import HTMLResponse

from fastapi.responses import Response
from fastapi import HTTPException
from datetime import datetime

app88 = FastAPI() # create an instance of the FastAPI class

@app88.get("/") #decorator provided by FastAPI
def read_root():#function for GET request  
    return {"Status": "alive! "}

@app88.get("/dbg") #decorator provided by FastAPI
def read_debag():#function for GET request  
    r = os.getcwd()
    return r

@app88.get("/w_list")
def wlist():      
    # read sql
    with open(r"../_sqlapi/Query08api1.sql", "r") as file: 
        sql = file.read() 
    conn = sqlite3.connect(r"../wine.db")
    w0,r = 0,"<body>"
    r+=r"<strong>THE LIST OF WINES</strong>" + "\n"    
    r+= r'<em>This is a list of the various wines in stock.'+ "\n"
    r+= r'Click on the "find substitutes" link to see the 5 most popular alternatives carefully selected based on taste, price and rating.'
    r+="</em>"+"\n"+"<pre>----------------------------------------------------------------------\n"
    for row in conn.cursor().execute(sql): 
        r += row[0] + rf' <a href="/substitutes/{row[2]}">find substitutes</a>' + "\n"       
    r += "-------------------------------------------------</pre>\n search string: ---" + "\n  "  
    r += str(datetime.now())[:19] + "\n" + "</body>"    
    r = r.replace('\n', '<br>')#.replace(' ', '&nbsp;').replace('\n', '<br>')
    r = Response(content= r, media_type="text/html")  
    return r 

@app88.get("/substitutes/{wine}")
def read_item_finder(wine: str):#, q: Union[str, None] = None):
    # read sql
    with open(r"../_sqlapi/Query08api4.sql", "r") as file: sql = file.read()
    wine = wine.replace(' ','%')
    sql=sql.replace('@VINE',"" + wine + "")
    # connect to db
    conn = sqlite3.connect(r"../wine.db") 
    # put response to text variable
    w0,r = 0,""    
    r+= r"<strong>THE LIST OF ALTERNATIVES FOR THIS WINE:</strong>" + "\n"
    r+= r"<em>Wine for which we are looking for a replacement are highlighted in bold." + "\n"
    r+= r"Alternatives with similar taste, rating, and price are shown in regular font"+ "\n"
    r+= "</em><pre>"
    r+= r" TYPE             NAME                                               WINARY   RATING   PRICE   OLDEST            TASTE" + "\n"
    r+= r"                  OF WINE                                            ID       AVARAGE  EUR/1L  3_YEARS           CONFIRMATIONS " + "\n"   
    x=1
    for row in conn.cursor().execute(sql): 
        w1,w2 = row[2],row[3]
        if w1==w2:           
            r += '<strong>' + "the original:     " + row[0]  + '</strong>' #+'\n'            
            x+=1
        else: 
            r += ' the substitute:  ' + row[1]        
        r += "\n"                

    r += "</pre>\n"
    r += str(datetime.now())[:19] + "\n"  
    r = r.replace('\n', '<br>').replace(' ', '&nbsp;').replace('\n', '<br>')   
    r = Response(content= r, media_type="text/html")
    return r 
        
