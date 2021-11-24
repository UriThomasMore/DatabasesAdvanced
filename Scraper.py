from bs4 import BeautifulSoup
import requests
import pandas as pd
import schedule
import time
from pymongo import MongoClient
import redis

# functie om hash-gegevens aan een overzichtslijst toe te voegen
def addhash(hashelement,overviewlist):
    for index, item in enumerate(hashelement):
        overviewlist.append([])
        overviewlist[index].append(item.getText())
    return overviewlist

# functie om timestamp, BTC en USD aan overzichtslijst toe te voegen
def addelements(elements,overviewlist): 
    index=0
    i=0
    for item in enumerate(elements):        
        overviewlist[index].append(item[1].getText())    
        i+=1  
        if i==3: 
            index+=1
            i=0

# functie waarmee een pandas dataframe wordt aangemaakt om de binnenkomende waarden toe te voegen aan een csv-file
def createdataframe(overviewlist): 
    df= pd.DataFrame(overviewlist, columns =['Hash', 'Timestamp', 'BTC', 'USD']) 
    df['USD'] = df['USD'].str.replace('$', '',regex = True)
    df['USD'] = df['USD'].str.replace(',', '',regex =True)
    df['USD'] = df['USD'].astype(float) 
    df.to_csv('test.csv',mode ='a',header = False, index =False)   
    return  df

# functie om na te gaan of er gegevens kunnen weggeschreven worden naar de logfile 'timestamp'
def checkcurrentoverview(newtimestamp):
     
     #Aanmaken nieuw pandas dataframe op basis van bewaarde overzichtslijst
     col_names =['Hash', 'Timestamp', 'BTC', 'USD']   
     current_overview = pd.read_csv('test.csv',names=col_names)
     #We selecteren de eerste aanwezige timestamp    
     currenttimestamp=current_overview.iloc[1]['Timestamp']      
     
     #We vergelijken deze eerste aanwezige timestamp met de eerste aanwezige timestamp van de laatste scrape die we uitgevoerd hebben.
     #Zijn deze niet gelijk dan schrijven we de hoogste score van bitcoins met dezelfde datum als de eerste aanwezige timestamp weg naar de logfile. 
     if newtimestamp != currenttimestamp:               
          #Aanmaken van nieuw dataframe op basis van datum currenttimestamp en ordenen op basis van hoogste dollar-waarde
          rslt_df = current_overview.loc[current_overview['Timestamp']==currenttimestamp] 
          rslt_df =rslt_df.sort_values(by='USD', ascending=False)    
                  
          timestampresult =rslt_df.values.tolist()
          timestampstring = f"Timestamp: {timestampresult[0][1]} - Hash: { timestampresult [0][0]} - BTC : {timestampresult [0][2]} - 'USD: {timestampresult [0][3]}'"          

          '''with open('timestamps.txt', 'a') as f:
              f.write('\n'+timestampstring )
              f.close()
          print("Saved to timestamp")'''

          #Timestamp toevoegen aan Redis-cache in container
          redisStart = redis.Redis(host='0.0.0.0',port='6379')
          redisStart.set("Highest",timestampstring, ex=45)
          timestampRedis=redisStart.get('Highest').decode("utf-8")          
          listmongodb= timestampRedis.split('-')       
          
          
          #Timestamp toevoegen aan MongoDBDatabase in container vanuit Redis-cache
          client = MongoClient("mongodb://localhost:27017/")
          db = client.Blockchain
          timestamp = {"Timestamp": listmongodb[0].split(':',1)[1],"Hash":listmongodb[1].split(':')[1], "BTC": listmongodb[2].split(':')[1],"USD": listmongodb[3].split(':')[1]}
          timest = db.Timestamps
          timest.insert_one(timestamp)
          print("Saved in mongoDB")
                    
          #Verwijderen van alle gegevens uit het dataframe met een gelijke timestamp van degene die we juist naar het logfile hebben weggeschreven en updaten van csv-file. 
          newcurrentoverview =current_overview[current_overview['Timestamp'] != currenttimestamp]     
          newcurrentoverview.to_csv('test.csv',mode ='w',header = False,index =False)          
          
     else: 
          print("Scraping")
     

#functie om scrapes uit te voeren en selecties te maken die kunnen weggeschreven worden naar logfile. 
def scraper():  
    
    #Scrapen van website voor hash, timestamp, BTC & USD
    url = 'https://www.blockchain.com/btc/unconfirmed-transactions'
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    elements = soup.find_all(class_ = 'sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC')
    hashelement = soup.find_all(class_ = 'sc-1r996ns-0 fLwyDF sc-1tbyx6t-1 kCGMTY iklhnl-0 eEewhk d53qjk-0 ctEFcK')
    
    #Opstellen van overzichtslijst
    overviewlist = []
    addhash(hashelement,overviewlist)    
    addelements(elements, overviewlist)
    new_timestamp = overviewlist[0][1]    
        
    createdataframe(overviewlist)    
    checkcurrentoverview(new_timestamp)
    

