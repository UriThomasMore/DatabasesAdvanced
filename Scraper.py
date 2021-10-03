from bs4 import BeautifulSoup
import requests
import pandas as pd
import schedule
import time
from csv import writer

def addhash(hashelement,overviewlist):
    for index, item in enumerate(hashelement):
        overviewlist.append([])
        overviewlist[index].append(item.getText())
    return overviewlist

def addelements(elements,overviewlist): 
    index=0
    i=0
    for item in enumerate(elements):        
        overviewlist[index].append(item[1].getText())    
        i+=1  
        if i==3: 
            index+=1
            i=0

def createdataframe(overviewlist): 
    df= pd.DataFrame(overviewlist, columns =['Hash', 'Timestamp', 'BTC', 'USD']) 
    df['USD'] = df['USD'].str.replace('$', '',regex = True)
    df['USD'] = df['USD'].str.replace(',', '',regex =True)
    df['USD'] = df['USD'].astype(float) 
    df.to_csv('test.csv',mode ='a',header = False, index =False)   
    return  df

def savedataframetocsv(timestamp,df): 
    df.to_csv(f'/home/udhaesel/Desktop/Dataframe/file{str(timestamp)}.csv', header = True,index=True)

def updatecurrentoverview(newtimestamp):
     
     col_names =['Hash', 'Timestamp', 'BTC', 'USD']
   
     current_overview = pd.read_csv('test.csv',names=col_names)     
     currenttimestamp=current_overview.iloc[1]['Timestamp']      
     
     if newtimestamp != currenttimestamp:               
          rslt_df = current_overview.loc[current_overview['Timestamp']==currenttimestamp] 
          rslt_df =rslt_df.sort_values(by='USD', ascending=False)    
                  
          timestampresult =rslt_df.values.tolist()
          timestampstring = f"Timestamp: {timestampresult[0][1]} - Hash: { timestampresult [0][0]} - BTC : {timestampresult [0][2]} - USD: {timestampresult [0][3]}"          

          f= open("printedtimestamps.txt","w+")
          f.close()
          a_file = open("printedtimestamps.txt", "r")
          overviewtimestamps = []
          for line in a_file:                
                overviewtimestamps.append(line)
                   
          if timestampresult[0][1] not in overviewtimestamps:
               with open('timestamps.txt', 'a') as f:
                    f.write('\n'+timestampstring )          
                    f.close()
               with open('printedtimestamps.txt', 'a') as f:
                    f.write(timestampresult[0][1])
                    f.close()
               print("Saved to timesamp")
          
          newcurrentoverview =current_overview[current_overview['Timestamp'] != currenttimestamp]     
          newcurrentoverview.to_csv('test.csv',mode ='w',header = False,index =False)
          savedataframetocsv(newcurrentoverview.iloc[1]['Timestamp'],newcurrentoverview)
          
     else: 
          print("Scraping")
     

def scraper():    
    url = 'https://www.blockchain.com/btc/unconfirmed-transactions'
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    elements = soup.find_all(class_ = 'sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC')
    hashelement = soup.find_all(class_ = 'sc-1r996ns-0 fLwyDF sc-1tbyx6t-1 kCGMTY iklhnl-0 eEewhk d53qjk-0 ctEFcK')
    
    overviewlist = []
    addhash(hashelement,overviewlist)    
    addelements(elements, overviewlist)
    new_timestamp = overviewlist[0][1]
     
        
    df_result= createdataframe(overviewlist)    
    updatecurrentoverview(new_timestamp)
    
    

schedule.every(15).seconds.do(scraper)

while True: 
    schedule.run_pending()
    time.sleep(15)