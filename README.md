#Requirements
In order to use this script, you'll need

1. Python (I tested on 2.7.6 and 3.4)
2. [BeautifulSoup version 4](http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)

I believe everything else I use is from the standard library.

#Using the tool
From terminal, simply run

    $ python Roshpit.py

The output will be of the form:

    Top five gold users:
    |gianmk      |8 x|3000     |3510       
    |dabbie      |1 x|2160     |5726       
    |Rocco       |4 x|949      |9561       
    |The Whip    |1 x|757      |2565       
    |szuturon    |8 x|750      |25320      
    
    Top five silver users:
    |phoogeh     |1 x|50       |322874     
    |T1nn3r      |3 x|50       |118168     
    |GaM3r       |4 x|50       |90336      
    |Newton      |1 x|0        |88362      
    |SpawnRulz   |3 x|0        |79155

where (columnwise), we present the users' names, multipliers, outstanding gold bets and silver balances.
