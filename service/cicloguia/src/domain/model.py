from collections import namedtuple

from icecream import ic

fields = (
    'url',
    'scraping_date',
    'product_name',  # todo: rename to name within the web scraper
    'brand',
    'categories',
    'sku',
    'price',
    'description',
    'specifications',
    'alert',
    'sizes',
    'unavailable_sizes',
    'image_urls',
    'images',
)
Product = namedtuple('Product', fields)

if __name__ == '__main__':
    example_product = Product(*range(12))
    ic(example_product)
