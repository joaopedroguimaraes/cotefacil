import scrapy


class PedidoItem(scrapy.Item):
    motivo = scrapy.Field()
    itens = scrapy.Field()


class ProdutoItem(scrapy.Item):
    codigo_produto = scrapy.Field()
    descricao = scrapy.Field()
    quantidade_faturada = scrapy.Field()
