import json
import os
import re

from dotenv import load_dotenv
from nacl.encoding import HexEncoder
from nacl.public import SealedBox, PublicKey
from scrapy import FormRequest, Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..items import ProdutoItem


# def url_can_be_scraped(url):
#     return re.match(r'.*/loja/[a-zA-Z]+/[0-9]+$', url) is not None


class ProdutosSpider(CrawlSpider):
    name = "produtos"
    allowed_domains = ["www.compra-agora.com"]
    URL_BASE = "https://www.compra-agora.com"
    URL_ARTIGO = "https://www.compra-agora.com" \
                 "/artigo/trocasdevolucoes"
    URL_LOGAR = f"{URL_BASE}/cliente/logar"
    start_urls = [URL_BASE]

    rules = [
        Rule(LinkExtractor(
            # allow=[r'/loja\/[a-zA-Z]+\/[0-9]+'],
            allow=['/loja/'],
            deny=['Filtros', 'Marcas', 'Fabricantes', 'SubCategorias',
                  'filtro_principal']),
            callback='parse_produtos',
            follow=True)
    ]

    def start_requests(self):
        yield Request(self.URL_ARTIGO,
                      callback=self.parse_login)

    # def parse_start_url(self, response, **kwargs):
    #     yield Request(self.URL_ARTIGO,
    #                   callback=self.parse_login)

    def parse_login(self, response):
        public_key = [var_line for var_line in
                      [script for script in response.xpath('//script')
                       if 'PUBLIC_KEY' in script.get()][0]
                      .get().split('\n') if 'PUBLIC_KEY' in
                      var_line][0].strip().split('"')[1]
        public_key_bytes = public_key.encode('utf-8')

        load_dotenv()
        payload_json = {
            "usuario_cnpj": os.getenv("LOGIN_CNPJ"),
            "usuario_senha": os.getenv("LOGIN_SENHA"),
            "eub": "0",
            "recaptchaLoginToken": None
        }
        payload = json.dumps(payload_json).replace(" ", "") \
            .encode('utf-8')

        sealed_box = SealedBox(
            PublicKey(public_key_bytes, HexEncoder))
        encrypted = sealed_box.encrypt(payload, encoder=HexEncoder)

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        return FormRequest(
            url=self.URL_LOGAR,
            method="POST",
            formdata={'data': encrypted.decode('utf-8')},
            headers=headers,
            encoding='utf-8',
            callback=self.parse_after_logged_in
        )

    def parse_after_logged_in(self, response):
        response_login = json.loads(response.text)
        if response.status == 200 and response_login['success']:
            print("LOGOU COM SUCESSO")
            return [Request(url=u) for u in self.start_urls]
        else:
            print("DEU RUIM PRA LOGAR")
            return

    def parse_produtos(self, response):
        for element in response.xpath(
                "//div[@class='shelf-item-inner']"):
            produto = ProdutoItem()
            produto['descricao'] = element.xpath(
                ".//a[@class='produto-nome mb-1']/text()")\
                .get().strip()
            produto['fabricante'] = element.xpath(
                ".//a[@class='produto-marca mb-1']/text()")\
                .get().strip()
            produto['imagem_url'] = element.xpath(
                ".//div[@class='shelf-img']/figure/img/@data-src")\
                .get().strip()
            yield produto
