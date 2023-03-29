import sys

from scrapy import cmdline

if __name__ == '__main__':
    pedido_id = int(sys.argv[1])
    cmdline.execute(f"scrapy crawl pedido -a pedido_id={pedido_id} "
                    f"-O pedidos.json".split())
