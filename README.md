# DatabasesAdvanced

## Opdracht 1

Voorbereiding

  ◦ Install Python

  ◦ Install Linux – Xubuntu
      ▪ Adjust Linux settings : Language

  ◦ Download Anaconda : https://linuxize.com/post/how-to-install-anaconda-on-ubuntu-20-04/ 

  ◦ Install VSCode

  ◦ Start Anaconda: 

      ▪ $ source ~/anaconda3/bin/activate root
      ▪ $ anaconda-navigator

  ◦ Create Folder Databases

  ◦ Start Project in Visual code:
  
      ▪ Download BeautifulSoup : pip install beautifulsoup4 

Scraper

Mijn scraper bestaat 4 (hulp)-functie en één hoofdfunctie. Elke minuut wordt de webiste www.blockchain.com gescraped.  Deze gegevens worden toegevoegd aan een csv-file om zo tot een overzicht te komen.  Bij elke nieuwe scrape wordt er een vergelijking gemaakt tussen de meest recente timestamp van de nieuwe scrape en de eerste timestamp van de deze in de overzichtslijst. Als deze niet gelijk is dan worden de gegevens met deze laatste timestamp weggegeschreven van de timestamp en wordt de bitcoin met de hoogste waarde toegevoegd aan de logfile. 

![image](https://user-images.githubusercontent.com/91833234/135995766-58675c61-e3cf-42f8-ab17-cd28c5c45fa9.png)


![image](https://user-images.githubusercontent.com/91833234/135995096-170cb1af-143b-4ec7-a1ba-6797f32efdbb.png)

## Opdracht 2 

* Installeren van mongoDB op Linux
  Commands: 
    * wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -
    * echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
    * sudo apt-get update
    * sudo apt-get install -y mongodb-org
    
 * Opmaken van bashscript mongoDB om een instantie van de mongoDB server op te starten met de volgende commands
    * sudo systemctl start mongod
    * sudo systemctl enable mongod
    
 * Aanpassen van script Scraper zodat de bekomen timestamps worden opgeslagen in de mongoDB-database:
    ![image](https://user-images.githubusercontent.com/91833234/137693668-3d8dd5a9-d8d9-45b8-847e-1df106445434.png)

   Dit is het resultaat: 
   ![image](https://user-images.githubusercontent.com/91833234/137693544-1bd041da-d10d-48ea-bda0-10907f08a446.png)
  * Aanmaken van timer-script om elke minuut de website te scrapen: 
     ![image](https://user-images.githubusercontent.com/91833234/137693895-c8ef2f4c-2b03-437b-b5e1-4bc5d091e05b.png)

## Opdracht 3

* Installeren van Redis op Linux
  Commands: 
    * wget http://download.redis.io/redis-stable.tar.gz
    * tar xvzf redis-stable.tar.gz
    * cd redis-stable
    * make

* Aanpassen van script zodat resultaat voor 45 seconden in cache wordt geplaatst in Redis en dan wordt overgeschreven naar mongoDB
   
  ![image](https://user-images.githubusercontent.com/91833234/141132757-5756695a-ecee-4ea5-9dad-6fa5322fdea7.png)

* Resultaat in Redis: 

  ![image](https://user-images.githubusercontent.com/91833234/141133037-98b7d0c5-7a49-4349-b7b5-10e496d999fc.png)


* Resultaat in mongoDB

  ![image](https://user-images.githubusercontent.com/91833234/141133369-f9076062-6347-4103-a3b2-e7ed6bdc203d.png)

## Opdracht 4

* Installeren van Docker op Ubuntu: https://docs.docker.com/engine/install/ubuntu/ 

* Installeren van Image mongoDB en aanmaken container 
     Commands: 
        * docker pull mongo
        * docker run --name mongodb -d -p 27017:27017 mongo:latest

* Installeren van Image Redis en aanmaken container: 
      Commands: 
        * docker pull redis
        * docker run --name redisdb5 -d -p 6379:6379 redis

* Aanpassen van script zodat er wordt gebruik gemaakt van de Docker-containers en niet van de lokale databases: 
      mongoDB: 
      
      ![image](https://user-images.githubusercontent.com/91833234/143298771-268ef430-5f10-48f0-b400-b7c4cb6f53d5.png) 
      
      Redis: 
      
      ![image](https://user-images.githubusercontent.com/91833234/143299057-a88ea4ba-929a-458d-a06a-69b58bd1c585.png)

* Resultaat: 
      Scraper: 
      
      ![image](https://user-images.githubusercontent.com/91833234/143299217-64e4301c-3209-4f08-a03d-6e87b07f25a8.png)
      
      mongoDB: 
      
      ![image](https://user-images.githubusercontent.com/91833234/143299419-8c20bd9b-08f5-42fb-9e85-8728f953b762.png)      
      ![image](https://user-images.githubusercontent.com/91833234/143299793-bde642ea-32ea-454d-8c2f-d8a43c9ba815.png)

      

      
     



   
  




