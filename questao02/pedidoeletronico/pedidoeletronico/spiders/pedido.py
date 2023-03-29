import json
import logging
import os

import jwt
import scrapy
from dotenv import load_dotenv
from scrapy import Request

from ..items import PedidoItem, ProdutoItem


def decode_jwt(jwt_token):
    return jwt.decode(jwt_token, verify=False)


def errback_handling(response):
    return {'ERRO': response.request.cb_kwargs['message']}


class PedidoSpider(scrapy.Spider):
    name = "pedido"

    def __init__(self, pedido_id, *args, **kwargs):
        super(PedidoSpider, self).__init__(*args, **kwargs)
        self.pedido_id = pedido_id
        self.access_token = ''
        self.codigo_usuario = 0
        self.codigo_externo = 0

    def start_requests(self):
        load_dotenv()
        payload = {
            "usuario": os.getenv('LOGIN_USUARIO'),
            "senha": os.getenv('LOGIN_SENHA')
        }
        return [Request(
            url="https://peapi.servimed.com.br/api/usuario/login",
            method="POST",
            body=json.dumps(payload),
            headers={
                'content-type': "application/json",
                'cache-control': "no-cache"
            },
            callback=self.parse_after_login,
            errback=errback_handling,
            cb_kwargs={'message': 'FALHA NO LOGIN'}
        )]

    def parse_after_login(self, response, message):
        logging.warning("Login efetuado com sucesso")
        response_body = json.loads(response.body)
        self.codigo_usuario = response_body['usuario']['codigoUsuario']
        self.codigo_externo = response_body['usuario']['codigoExterno']
        jwt_token = [token.decode("utf-8") for token in response.headers.getlist('Set-Cookie')
                     if 'accesstoken' in str(token)][0].split('=')[1]
        self.access_token = decode_jwt(jwt_token)['token']

        logging.warning("Procurando pedido")
        payload = {
            "dataInicio": "",
            "dataFim": "",
            "filtro": self.pedido_id,
            "pagina": 1,
            "registrosPorPagina": 10,
            "codigoExterno": self.codigo_externo,
            "codigoUsuario": self.codigo_usuario,
            "users": [self.codigo_externo]}
        return Request(
            url="https://peapi.servimed.com.br/api/Pedido",
            method="POST",
            body=json.dumps(payload),
            headers={
                'content-type': "application/json",
                'cache-control': "no-cache",
                'loggeduser': self.codigo_usuario,
                'accesstoken': self.access_token
            },
            callback=self.parse_pedido
        )

    def parse_pedido(self, response):
        pedidos_lista = json.loads(response.body)['lista']

        if not len(pedidos_lista):
            logging.warning(f"Pedido {self.pedido_id} não encontrado")
            return {'ERRO': 'PEDIDO_NAO_ENCONTRADO'}

        logging.warning(f"Pedido {self.pedido_id} encontrado")
        url = f"https://peapi.servimed.com.br/api/Pedido/" \
              f"ObterTodasInformacoesPedidoPendentePorId/" \
              f"{pedidos_lista[0]['id']}"
        return Request(
            url,
            method="GET",
            headers={
                'content-type': "application/json",
                'cache-control': "no-cache",
                'loggeduser': self.codigo_usuario,
                'accesstoken': self.access_token
            },
            callback=self.parse
        )

    def parse(self, response, **kwargs):
        logging.warning(f"Retornando itens")
        response_data = json.loads(response.body)

        pedido = PedidoItem()
        pedido['motivo'] = response_data['rejeicao'].strip()
        logging.warning(f"Motivo: {pedido['motivo']}")
        pedido['itens'] = []

        for produto_data in response_data['itens']:
            produto = ProdutoItem()
            produto['codigo_produto'] = produto_data['produto']['codigoExterno']
            produto['descricao'] = produto_data['produto']['descricao']
            produto['quantidade_faturada'] = produto_data['quantidadeFaturada']
            pedido['itens'].append(produto)

        return pedido
