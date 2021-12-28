from collections import namedtuple

from icecream import ic

fields = (
    'url',
    'product_name',
    'brand',
    'category',
    'sku',
    'price',
    'description',
    'specifications',
    'alert',
    'sizes',
    'unavailable_sizes',
    'image_urls',
)
Product = namedtuple('Product', fields)

if __name__ == '__main__':
    example_product = Product(*range(12))
    ic(example_product)
