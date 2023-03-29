import scrapy


class ProdutoItem(scrapy.Item):
    descricao = scrapy.Field()
    fabricante = scrapy.Field()
    imagem_url = scrapy.Field()
