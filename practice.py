from collections import namedtuple

from icecream import ic

if __name__ == '__main__':
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
    example_product = Product(*range(12))
    ic(example_product)
    url, *others = example_product
    ic(url)
