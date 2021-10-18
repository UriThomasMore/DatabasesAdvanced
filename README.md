# DatabasesAdvanced

Opdracht 1

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
