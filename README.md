# pad-db

                                ----- UPDATE -----
        
        It seems my efforts were largely in vain. This project managed to get 
        partially deprecated just as quickly as it was built! LOL However, 
        I'll keep working towards my original goal
        as a test of my own ability, and start taking advantage of the now 
        open MiruBot API to wrap it in both a web and, eventual, iOS app probably.



TO RUN:
    
    1. Clone the project (duh)
    
    2. Build your database.. run the following:
    
        python3 manage.py makemigrations
        python3 manage.py migrate
        
    3. Collect cards using custom command:
        
        python3 manage.py updatecardsna
        
        (should take anywhere between 1-2 minutes usually)

    4. Run the server
        
        python3 manage.py runserver

New Goal :

    Make a wrapper for the Mirubot API for web.


If you would like to join my Discord development group to follow progress, use the link below.

    https://discord.gg/4MhSWuY
   

*** DEPRECATED ***

An open source, web-based utility to encourage crowdsourcing of data from within Puzzles and Dragons.

The interface allows a user to paste a web address to a PADx dungeon page, and gives the user back a model
with the parsed data from that dungeon. This is done on an individual basis, however, meaning that each individual
difficulty for a dungeon must be added (until I create a mechanism for multi-add).

 Current capabilities :

    1. Parse dungeon data : Titles, Stamina cost, floors, etc
    2. Parse encounter info (HP, ATK, DEF)
    3. Parse Skills of encounters (but not their thresholds)
    
    
Thanks to the following services:

    1. Django
    2. Bulma CSS
    