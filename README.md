This system is used to check the most played Heroes, Classes, and Origins in the Challenger league in Ranked Team Fight Tactics.

The system uses the Riot API to collect data from Brazilian players and we built 2 charts demonstrating the Pick Rate of both heroes and the abilities of these heroes.

The system collects data from 75 players (from the Challenger rank), where each match contains 8 players, and each player can contain several heroes, from 1 to 10, according to the Summoner Level.

The system collects 5 matches from each of the 75 players.

We extract data only from the TOP 4 players in each match, as these are the players who score points, and are the 'best of the match'.

From the selection of the TOP 4 players of each match, we calculate the Pick Rate of each hero and ability.

The system also operates at the speed limit of the API, without being blocked by excess requests and with no idle time.

It stores the data in a structured way inside RAM memory for faster access, and also to perform arbitrary queries with pandas.

Technologies used: Pydantic, Matplotlib, dotenv, httpx, Ruff

Installation guide for Linux/Ubuntu

1 - To reproduce:
  
  - clone the repository https://github.com/RenanMEvaristo/TFT-Data.git
  - install the dependencies with uv https://docs.astral.sh/uv/getting-started/installation/
  - use uv sync to download the correct versions

2 - Configure your RIOT API

  - Create a RIOT account on the website https://developer.riotgames.com/
  - Go to the main page, retrieve your API key
  - The key needs to be in an environment variable or, in the root folder of the project, create a file named .env

command: nano .env

  - paste your key in the standard format RGAPI_KEY=RGAPI-your-key-here-12345 and save.

3 - Running the project:

  - To run data mining and the report in the terminal command: uv run python src/main.py

  - To open the chart of the most played heroes command: uv run python src/graph_heroes.py

  - To open the chart of the most used abilities command: uv run python src/graph_traits.py

These commands will produce files in the TFT-Data/src folder
