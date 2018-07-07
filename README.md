# pad-cal
An open source, web-based utility to encourage crowdsourcing of data from within Puzzles and Dragons.

The interface allows a user to paste a web address to a PADx dungeon page, and gives the user back a model
with the parsed data from that dungeon. This is done on an individual basis, however, meaning that each individual
difficulty must be added (until I create a mechanism for multi-add)


 Current capabilities :

    1. Parse dungeon data : Titles, Stamina cost, floors, etc
    2. Parse encounter info (HP, ATK, DEF)
    3. Parse Skills of encounters (but not their thresholds)
    
    
Todo / In progress:

    1. Add more to the frontend
    2. Add asyncronous processing of the parse function
    3. Add some sort of multi-add + multi-select feature for dungeons

Requirements :

    1. A link to the dungeon page
    2. BeautifulSoup4
    3. Python 3
    4. html5lib or lxml
    5. Celery
    6. Django 2.0.7
    
    
Thanks to the following services:

    1. Django
    2. Bulma CSS
    
    


Here is some example output of parsed data..
    
![alt text](https://github.com/rohilthopu/pad-cal/blob/master/Screenshots/Screen%20Shot%202018-06-29%20at%201.20.29%20AM.png)
