# pad-db


Pad DB is a simple project of mine to wrap the data from within Puzzles and Dragons, using PadGuide data.

The app uses a set of custom Django commands to parse and load the data into Django models. 

Guerrilla dungeons and the karma leaderboards are updated regularly, with guerrillas updated every hour,
and karma every day.
   
Visit the project live at

    www.pad-db.com
    
    
RECENT CHANGES (v1.1):

    Added a Reddit /r/PAD karma leaderboard
        
        Tracks daily changes in karma for /r/PAD posters after the inital 250 top post collection.
        
    Added ability to edit monster data/values
    
    Added ability to edit active skill data/values
    
    Added ability to edit leader skill data/values
    
    Removed JP data from the site temporarily to focus on improving other stuff first. 
    
    Changed sorting options on the calendar tables so that both tables now use DataTables to organize and display stuff
    
    Re-enabled DataTables on the JP table
    
    Updated scripts for updatecardsna/updateskillsna to only collect most recent data, so as to preserve any changes that 
        might have been made to the db from the front end.
        
    Add a parser to parse basic information from the Dungeons API such as Floor drop data
    
    Added a page to list the dungeons with a drop down to select the difficulty level

    
    