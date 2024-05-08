# Database Application

## Seções
- [Sobre o projeto](#sobre-o-projeto)
    - [Tecnologias](#tecnologias)
- [Equipe](#equipe)
- [Datasets](#datasets)
- [Iniciando o banco de dados](#iniciando-o-banco-de-dados)
    - [Instalando o Docker](#instalando-o-docker)
    - [Iniciando o container](#iniciando-o-container)
    - [Acessando o banco de dados](#acessando-o-banco-de-dados)
    - [Finalizando o container](#finalizando-o-container)
    - [Erros conhecidos](#erros-conhecidos)

## Sobre o projeto
Trabalhar as capacidades de modelagem lógica e física, engenharia reversa a partir de um dataset pré-existente e utilização de bases de dados NoSQL.

### Tecnologias
Para este projeto, foi utilizada as seguintes tecnologias:
- [Docker](https://www.docker.com/), uma plataforma que permite separar as aplicações e facilitar o compartilhamento das mesmas.
- [Python](https://www.python.org/), uma linguagem de programação com uma sintaxe simples e pacotes complexos.
- [Pandas](https://pandas.pydata.org/), uma biblioteca para análise e manipulação de dados.
- [MySQL](https://www.mysql.com/), uma database relacional SQL.
- [MongoDB](https://www.mongodb.com/), uma database documental NoSQL.

## Equipe
- Carlos Alberto Ramalho - 01585045
- Gustavo Portela Pachêco - 01604533
- José Gabriel de Oliveira Lino - 01609620
- Marcio Sobel - 01578025
- Rafael Antônio Ribeiro Galvão Mendes - 01604007

## Datasets
O tema escolhido para o projeto foi [Pokémon](https://en.wikipedia.org/wiki/Pok%C3%A9mon).
Os datasets escolhidos para a aplicação foram [Pokemon Gen VII Pokedex with Moves](https://www.kaggle.com/datasets/csobral/pokemon-gen-vii-pokedex) e [Pokemon Sun and Moon (Gen 7) Stats](https://www.kaggle.com/datasets/mylesoneill/pokemon-sun-and-moon-gen-7-stats?select=type-chart.csv)

## Iniciando o banco de dados
Para iniciar o banco de dados, utilizaremos o `docker`. Se você já estiver com ele instalado ou já for familiarizado com, pode pular para a seção [Iniciando o banco de dados](#iniciando-o-banco-de-dados).

### Instalando o Docker

#### Windows
Primeiramente, tenha certeza que você possui o [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado.


Após isso, tenha certeza que o mesmo está aberto e a engine em execução. Você pode verificar isso escrevendo o seguinte código no terminal:
```
> docker -v
```
Você deve receber um resultado parecido com esse:
```
> docker -v
Docker version 26.1.1, build 4cf5afa
```

#### Linux
Primeiramente, tenha certeza que você possui o [Docker Engine](https://docs.docker.com/engine/install/) instalado (Recomendo o Docker Engine por ser mais rápido e leve que o Docker Desktop, mas caso use o desktop, você pode seguir os mesmos passos do [Windows](#windows)).

Após isso, tenha certeza que o mesmo está aberto e a engine em execução. Você pode verificar isso escrevendo o seguinte código no terminal:
```
$ docker -v
```
Você deve receber um resultado parecido com esse:
```
$ docker -v
Docker version 26.1.1, build 4cf5afa
```

### Iniciando o container
Para executar o container, basta executar o seguinte comando no terminal:
```
$ docker compose up -d
```
Se for sua primeira vez executando-o, ele irá baixar as imagens do [MySQL](https://hub.docker.com/_/mysql) e do [MongoDB](https://hub.docker.com/_/mongo). Após isso, o terminal estará livre para uso.

### Acessando o banco de dados
Para acessar o banco de dados, o seguinte comando:
```
$ docker exec -it [ID ou nome do container] bash
```
onde o `ID ou nome do container` podem ser encontrados no arquivo `docker-compose.yml` ou digitando o comando:
```
$ docker ps
``` 

### Finalizando o container
Para finalizar o container, basta executar o seguinte comando no terminal:
```
$ docker compose down
```

### Erros conhecidos
No Linux, pode acontecer da engine do docker não estar executando, gerando assim o seguinte erro:
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```
Para solucionar isso, basta iniciar a engine através do seguinte comando:
```
$ systemctl start docker
```
ou
```
$ systemctl start docker.socket
```
(O mesmo vale para parar a engine, apenas troque `start` por `stop`)
