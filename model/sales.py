from dataclasses import dataclass
from datetime import date


@dataclass
class Sale:
    Retailer_code: int
    Product_number: int
    Order_method_code: int
    Date: date
    Quantity: int
    Unit_price: float
    Unit_sale_price: float

    def __str__(self):
        return f"{self.Product_number} - {self.Retailer_code} - {self.Date}"

    def __hash__(self):
        return hash((self.Product_number, self.Retailer_code, self.Date))
