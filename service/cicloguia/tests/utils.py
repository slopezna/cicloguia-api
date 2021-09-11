from uuid import uuid4
from typing import Dict


def generate_random_string() -> str:
    return uuid4().hex


def generate_random_product_data() -> Dict:
    return {
        'url': f'https://www.{generate_random_string()}.cl',
        'product_name': f'fake_product_{generate_random_string()}',
        'category': f'fake_category_{generate_random_string()}',
        'brand': f'fake_brand_{generate_random_string()}',
    }
