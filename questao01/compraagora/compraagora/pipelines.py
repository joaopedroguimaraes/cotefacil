import json

from itemadapter import ItemAdapter
# from scrapy.exceptions import DropItem


class JsonWriterPipeline:

    def __init__(self):
        self.file = None
        # self.imagem_urls = set()

    def open_spider(self, spider):
        self.file = open('produtos.jsonl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        # Aqui daria pra usar o pandas e criar um df pra validar
        # a duplicidade de itens

        # adapter = ItemAdapter(item)
        # if adapter['imagem_url'] in self.imagem_urls:
        #     raise DropItem(f"Duplicate item found: {item!r}")
        # else:
        #     self.imagem_urls.add(adapter['imagem_url'])
        #     return item

        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item
