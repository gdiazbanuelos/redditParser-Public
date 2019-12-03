# Reddit Parser
> A bot that parses Reddit!

This a collection of my reddit parsers!
In each folder is a script.sh that executes the bot that scans
the specific subreddit for the specific game in 60 second intervals


## Set up the bot

** To get the Reddit __client_id__ and __client_secret__ **

1. Go to your Reddit account -> preferences -> apps. Create another app, give the bot a name and description. Select the script option and fill in about and redirect to anything. The client id and client secret values will be given to you. Fill in those values and the reddit username and password in the respective boxes.

2. To run the Scripts in 60 second intervals in the background:
    * cd into the desired subreddit bot folder, this is the 3DS example

        * 1. $ cd 3DS_Deals_Bot
        * 2. $ nohup ./Script_3DS.sh &

You are done! The bot will run in the background and scan every 60 seconds
