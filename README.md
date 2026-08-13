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

#####################################################################################################################################################################

Este sistema é utilizado para verificar os Heróis, Classes e Origens mais utilizadas na liga Challenger no Team Fight Tatics Rankeado.

O sistema utiliza a API da Riot para a coleta dos dados de jogadores Brasileiros e construimos 2 gráficos demonstrando o Pick Rate tanto de heróis quanto das Habilidades desses heróis.

O sistema coleta os dados de 75 jogadores(do rank Challenger), onde cada partida contem 8 jogadores, e cada jogador pode conter vários heróis, de 1 a 10, de acordo com o Nivel do Invocador.

O Sistema coleta 5 partidas de cada um dos 75 jogadores.

Retiramos os dados apenas do TOP 4 jogadores em cada Partida, pois estes são os jogadores que pontuam, e são os 'melhores da partida'.

A partir da selação do TOP 4 jogadores de cada partida, calculamos o Pick Rate de cada heroi e habilidades.

O sistema também opera no limite de veloidade da API, sem ser bloqueado por excesso de requisição e sem tempo parado.

Guarda os dados de forma estruturada dentro da memoria ram para ter um acesso mais rapido, e também fazer consultas arbritárias com pandas.

Tecnologias utilizadas: Pydantic, Matplotlib, dotenv, httpx, Ruff

-----

Guia para instalação em Linux/Ubuntu

1 - Para reproduzir:
- clone repositório https://github.com/RenanMEvaristo/TFT-Data.git
- instale as dependências com uv https://docs.astral.sh/uv/getting-started/installation/
- use uv sync para baixar as versões corretas

2 - Configure sua API da RIOT

- Crie uma conta da RIOT no site https://developer.riotgames.com/
- Vá na pagina principal, resgate sua chave API
- A chave precisa estar em uma variavel de ambiente ou, na pasta raiz do projeto crie  um arquivo chamado .env

comando: nano .env

- cole a sua chave no formato padrao RGAPI_KEY=RGAPI-sua-chave-aqui-12345 e salve.

3 - Rodando o projeto:

- Para rodar a mineração e o relatório no terminal
comando: uv run python src/main.py

- Para rodar abrir o gráfico dos herois mais jogados

comando: uv run python src/graph_heroes.py

- Para abrir o gráfico de habilidades mais usadas
comando: uv run python src/graph_traits.py


Esses comandos vão produzir arquivos na pasta TFT-Data/src
