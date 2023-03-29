# Questão 2

## Objetivo
Obter o retorno de faturamento do pedido que o usuário informar ao executar.
Ao final, deve ser gerado um arquivo `.json` com as informações obtidas.

## Overview técnico
- Versão do Python: 3.10
- Último acesso ao site: 27/03/2023
- Framework principal: Scrapy

Em uma análise inicial das requisições do site, percebi que utilizava-se uma
API. Por isso, foquei o procedimento do _spider_ em requisições para a URL
dessa API.

Para o acesso ao site, identifiquei que utilizava-se um token JWT e, por isso,
utilizei a biblioteca `PyJWT` para capturar o _access token_ utilizado nas
requisições.

## Executando

**ATENÇÃO!** Por segurança, as credenciais de acesso utilizadas não foram
expostas no escopo do projeto. Para configurá-las, utilize o arquivo `.env.example`
como um modelo e crie um arquivo `.env` no mesmo repositório que se encontra o
modelo, inserindo corretamente as credenciais necessárias. 

### Terminal
Após clonar o repositório, ter a versão do Python compatível instalada e ter
criado o arquivo `.env` com as credenciais, é necessário ativar o `venv`
dentro da pasta `/questao02`.

Em seguida, ainda nesse diretório, execute o comando abaixo para
instalar as bibliotecas necessárias:

```
pip install -r requirements.txt
```

O _pip_ se encarregará de instalar as bibliotecas nas versões especificadas
pelo arquivo _requirements.txt_.

Por fim, para a execução do projeto, você deve entrar no diretório do projeto
Scrapy e executar o arquivo `main.py` informando como argumento do comando o
número do pedido a ser pesquisado:

```
Terminal:

cd pedidoeletronico/
python main.py <numero_do_pedido>
```

Substitua `<numero_do_pedido>` pelo número do pedido, como o exemplo abaixo:

```
Terminal:

python main.py 511082
```

Feito isso, você já verá a execução do _spider pedidos_. Ao final da execução,
é gerado o arquivo `pedidos.json` nesse mesmo diretório.

### Docker
Para executar utilizando o Docker, você deve ter o Docker instalado e ter
criado o arquivo `.env` com as credenciais.

Com ele instalado corretamente, vá para o diretório `questao02` do projeto,
onde há o arquivo `Dockerfile`. Nesse diretório, execute o comando
seguinte pelo terminal:

```
Terminal:

docker build -t questao02 .
```

Quando a imagem estiver pronta, você pode subí-la/executá-la com o número do
pedido a ser pesquisado:

```
Terminal:

docker run questao02 <numero_do_pedido>
```

Substitua `<numero_do_pedido>` pelo número do pedido, como o exemplo abaixo:

```
Terminal:

docker run questao02 511082
```

Feito isso, você já verá a execução do _spider pedidos_. Ao final da execução,
é gerado o arquivo `pedidos.json`.