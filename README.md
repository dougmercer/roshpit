#Requirements
In order to use this script, you'll need

1. Python (I tested on 2.7.6 and 3.4)
2. [BeautifulSoup version 4](http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)

I believe everything else I use is from the standard library.

#Description
This module is a web scraper for roshpit.ca. As the need to grab other data arises, I'll add to the module. For the time being, however, the only use of the tool is to list the five users with the greatest outstanding gold bets, along with their usernames, current multipliers, and silver balances. 

It also outputs the five players with the greatest silver balances, though this is can be found easily by inspection using the site's silver ladder directly. It is included only as a convenience, as it helps users who have the "dark patterns" tech weigh their options (i.e., if there is a player with, say, 350,000 silver, it might be best to simply cast occuli on that target to receive the guaranteed 3.5k exp). 

#Use
From terminal, simply run

    $ python Roshpit.py

The script takes about 42 seconds to run on my current internet connection (though I'm on a pretty poor internet connection, as I'm pushing this while travelling). This checks the top 50 users on the gold ladder and returns the five with greatest outstanding gold bets.

If you want to check a greater or lesser number of users on the gold ladder, simply pass a command line argument in the following manner (e.g., 100, to check the top 100 gold users):

    $ python Roshpit.py 100

Note that you may pass an arbitrarily large number, say, 1000000, and the application will check all users on the gold ladder.

#Output
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

#Future Work
I'm open to expanding this scraper in any way that might be useful to users. However, in the immediate future I plan on

1. Making the Top 5 Silver table optional
2. Including a column specifying the user's current faction
