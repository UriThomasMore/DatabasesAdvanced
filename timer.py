import schedule
import time
import Scraper

print('Scraping has started.You will have to wait one minute for anything happens')
schedule.every(60).seconds.do(Scraper.scraper)

while True: 
    schedule.run_pending()
    time.sleep(60)