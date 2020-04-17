# Pandora's Bot
It's an arcade bot

## Setup/Instructions CLI
1. cd to the project folder
2. run `python -m venv env`. This will create a virtual environment named 'env' in your project folder
3. With terminal/bash use `source env/scripts/activate` to activate the environment. With Command Prompt, cd into scripts and run activate.
4. run `pip install -r requirements.txt`. This will install discord.py and whatever else is included in requirements.txt
5. Drop `.env` into the project files. This file is pinned in the discord server
6. Run main.py and the bot should come online and be usable.

----

### Games and Game Commands
	
	Tic-Tac-Toe:
* How to Play - !t or !ttt + @Player

* Pick a Spot - Simply choose a number "*0 - 9*"
	
----

    Hangman: 
* How to Play - !hangman or !h or !hm + @Player

* Guess a Character - Simply type any character 

----

    Rock-Paper-Scissors
* How to Play - !rps + @Player

* Choose an option - Type "rock", "paper", or "scissors"

----

    Battleship:
* How to Play - !bs + @Player

* Place Ships:
    * 1st Step: Choose positioning, either horizontal or vertical  
    * 2nd Step: Choose starting coordinate and ending coordinate for the
     ship (Ex: A1 - A4)
    
* Guess Coordinate - !shoot + Coordinate (Ex: B6)
----

### Commands
- Help command - !h + number "*1 - 3*"
    - List of games (!h 2)
- Invite a player - *Incomplete*
- Check leaderboard - *Incomplete*
- Prize system (Role upgrades) - *Incomplete*
- Check player stats - *Incomplete*
  - Currency
  - Level
  - Win-Loss Ratio
  - Games played
  
----
  
### Other Ideas 

- Bingo?
- Slots/Gambling/Betting
- Leveling System
 
  
  [Invite Link](https://discordapp.com/api/oauth2/authorize?client_id=682350831429091357&permissions=268545104&redirect_uri=https%3A%2F%2Fdiscordapp.com%2Fapi%2Foauth2%2Fauthorize%3Fclient_id%3D682350831429091357%26permissions%3D0%26scope%3Dbot&scope=bot)
