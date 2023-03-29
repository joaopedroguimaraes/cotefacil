# Questão 2

## Objetivo
Realizar o login na plataforma Compra Agora e, em seguida, extrair 
todos os produtos e suas respectivas informações (descrição, 
fabricante e url da imagem), assim gerando elementos `json` e
salvando tudo em um arquivo `.jsonl`.

## Overview técnico
- Versão do Python: 3.10
- Último acesso ao site: 28/03/2023
- Framework principal: Scrapy

A primeira requisição da Spider Produtos obtém a `PUBLIC_KEY` exposta
em uma _tag_ `<script>` e permite as operações com a biblioteca
`PyNaCl`, com a qual efetuei o login diretamente pela url da
requisição (`/cliente/logar`) e, confirmando o sucesso no login, 
desenvolvi os parses para os produtos.

O Spider Produtos é um CrawlSpider, para que possa utilizar-se de
regras e extratores de link do Scrapy para realizar o _crawl_ pelo
site inteiro.

Optei pelo `.jsonl` ao invés de um arquivo `.json` por não ter 
estimativa de tamanho final do arquivo, uma vez que essa informação
depende inteiramente da plataforma de terceiro.

O fluxo de _scrape_ de cada Produto é tratado pela 
`JsonWriterPipeline`, que salva as informações do Item em JSON após a
conversão. Também deixei em aberto a possibilidade de utilizar o
`pandas` para a criação de um _dataframe_ a fim de fazer validações
_on the run_ de duplicidade de itens.

## Executando

**ATENÇÃO!** Por segurança, as credenciais de acesso utilizadas não foram
expostas no escopo do projeto. Para configurá-las, utilize o arquivo `.env.example`
como um modelo e crie um arquivo `.env` no mesmo repositório que se encontra o
modelo, inserindo corretamente as credenciais necessárias. 

### Terminal
Após clonar o repositório, ter a versão do Python compatível instalada e ter
criado o arquivo `.env` com as credenciais, é necessário ativar o `venv`
dentro da pasta `/questao01`.

Em seguida, ainda nesse diretório, execute o comando abaixo para
instalar as bibliotecas necessárias:

```
pip install -r requirements.txt
```

O _pip_ se encarregará de instalar as bibliotecas nas versões especificadas
pelo arquivo _requirements.txt_.

Por fim, para a execução do projeto, você deve entrar no diretório do projeto
Scrapy e executar o arquivo `main.py`, que executará o _crawl_:

```
Terminal:

cd compraagora/
python main.py
```

Feito isso, você já verá a execução do _spider Produtos_. Ao final da execução,
é gerado o arquivo `produtos.jsonl` nesse mesmo diretório.

### Docker
Para executar utilizando o Docker, você deve ter o Docker instalado e ter
criado o arquivo `.env` com as credenciais.

Com ele instalado corretamente, vá para o diretório `questao01` do projeto,
onde há o arquivo `Dockerfile`. Nesse diretório, execute o comando
seguinte pelo terminal:

```
Terminal:

docker build -t questao01 .
```

Quando a imagem estiver pronta, você pode subí-la/executá-la:

```
Terminal:

docker run questao01
```

Feito isso, você já verá a execução do _spider Produtos_. Ao final da execução,
é gerado o arquivo `produtos.jsonl`.