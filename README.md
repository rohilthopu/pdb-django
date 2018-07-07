# pad-cal
An open source, web-based utility to encourage crowdsourcing of data from within Puzzles and Dragons.

The interface allows a user to paste a web address to a PADx dungeon page, and gives the user back a model
with the parsed data from that dungeon. This is done on an individual basis, however, meaning that each individual
difficulty for a dungeon must be added (until I create a mechanism for multi-add).


If you would like to join my Slack group, I have created an open invite for people to use

    https://goo.gl/emtNQB
    
If you would like to contribute to the project, go ahead and fork and submit pull requests for substantial changes and I'll
check them out and consider incorporating them.

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
    
    
    
Updated Screenshots (July 7, 2018)

![alt text](https://github.com/rohilthopu/pad-cal/blob/master/Screenshots/Screen%20Shot%202018-07-07%20at%205.00.03%20PM.png)    
![alt text](https://github.com/rohilthopu/pad-cal/blob/master/Screenshots/Screen%20Shot%202018-07-07%20at%205.00.21%20PM.png)    
![alt text](https://github.com/rohilthopu/pad-cal/blob/master/Screenshots/Screen%20Shot%202018-07-07%20at%205.00.36%20PM.png)    
    


Outdated Screenshots:    
![alt text](https://github.com/rohilthopu/pad-cal/blob/master/Screenshots/Screen%20Shot%202018-06-29%20at%201.20.29%20AM.png)
