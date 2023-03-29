# Questão 6

O objetivo dessa questão era um scraper do site 
[Quotes to Scrape](http://quotes.toscrape.com/) de acordo com um autor
que fosse passado como parâmetro para a execução do script, 
obtendo suas informações e suas frases.

## Overview técnico
- Versão do Python: 3.10
- Último acesso ao site: 25/03/2023
- Framework principal: Selenium

Para representar um autor e suas frases obtidas do site em questão, 
criei classes (`Author` e `Quote`) e as relacionei para melhor
visualizar os dados e depois convertê-los em `json`.

Utilizando o framework Selenium, o _script_ acessa o site e busca 
pelas páginas se há o autor pesquisado. Se sim, guarda o número dessa
página e clica no `about`, obtendo ali todas as informações 
disponíveis do autor. Com o número da página, o _loop_ inicia 
novamente mas a partir da primeira página em que consta uma frase do
autor, a fim de reduzir custo de processamento (infímio, mas sempre
é bom pensar em escalabilidade de aplicações). Dali, segue fazendo o
_scrape_ de todas as frases do autor e suas tags.

Por fim, gera um arquivo `.json` com todos os dados.

O arquivo `main.py` pode ser executado por comando passando um autor
como parâmetro; o arquivo `run.py` chamará o arquivo `main.py` mas já
com o parâmetro do teste ("J.K. Rowling"), que inclusive também será
o arquivo a ser executado no Docker.

## Executando

### Terminal
Após clonar o repositório e ter a versão do Python compatível 
instalada, é necessário ativar o `venv` dentro da pasta `/questao06`.

Em seguida, ainda nesse diretório, execute o comando abaixo para
instalar as bibliotecas necessárias:

```
pip install -r requirements.txt
```

O _pip_ se encarregará de instalar as bibliotecas nas versões especificadas
pelo arquivo _requirements.txt_.

Por fim, para a execução do projeto, você deve entrar no diretório do projeto
Scrapy e executar o arquivo `run.py`, que executará o _crawl_:

```
Terminal:

python run.py
```

Feito isso, você já verá a execução do Selenium. Para melhor 
visualização optei por não colocar o atributo `headless`, por se 
tratar de um teste avaliativo e a observação da execução ser possível.
Ao final da execução, é gerado o arquivo `output.json` nesse mesmo 
diretório.

### Docker
Para executar utilizando o Docker, você deve ter o Docker instalado.

Com ele instalado corretamente, vá para o diretório `questao06` do projeto,
onde há o arquivo `Dockerfile`. Nesse diretório, execute o comando
seguinte pelo terminal:

```
Terminal:

docker build -t questao06 .
```

Quando a imagem estiver pronta, você pode subí-la/executá-la:

```
Terminal:

docker run questao06
```

Feito isso, o _script_ começará a execução e fará o _scrape_ das 
informações de autor e frases presentes no site. Ao final da execução,
é gerado o arquivo `output.json`.