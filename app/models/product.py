from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    serial_number: int
    product_name: str
    input_image_urls: List[str]
    output_image_urls: List[str] = list  # Correct way to set default list
