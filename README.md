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

1 -Para reproduzir:
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
