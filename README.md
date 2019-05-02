# PAD DB (Web)

PAD DB is a pet project of mine to provide access to Puzzle and Dragons (PAD) data in an 
alternative source to already existing platforms. This specific repository refers to the 
desktop version usable via any browser. 

See the site [here](www.pad-db.com)

The site provides access to Guerrilla Dungeons, Monsters, Dungeon information, and an 
arbitrary Reddit karma leaderboard for the PAD subreddit.

This site is meant to be a side resource to the mobile app, as the main goal is to just provide API
access to my mobile app, [PAD DB (iOS)](https://github.com/rohilthopu/pdb-swift). Having a web interface
helps me more easily visualize what the data currently looks like and helps me find errors in my code.

## Stack

Backend

    1. Django
    2. Python
    3. PostgreSQL

Frontend

    1. Django (Yikes)
    2. Bulma CSS
         
TODO:

    1. Docker integration
    2. ElasticSearch
    3. Separate parser from Django
        * Add multiprocessing/multithreading?
    4. Make dedicated frontend with React?
    5. Fix broken parsing for the wave data since the complete zip no longer available
    

## Installation

It's not worth it.

## Contributions

I'm probably not taking contributions for this right now, unless you can write a React frontend for me lol. 
