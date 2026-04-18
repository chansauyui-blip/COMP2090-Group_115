from abc import ABC, abstractmethod

class Product(ABC):
    VALID_SIZES = ["small", "medium", "large", "extra-large"]
    
    def __init__(self, item_id, name, price, quantity, size):
        self._item_id = item_id
        self._name = name
        self._price = price
        self._quantity = quantity
        self._size = self._validate_size(size)
    
    @abstractmethod
    def get_product_type(self):
        pass
    
    @staticmethod
    def _validate_size(size):
        if size.lower() not in Product.VALID_SIZES:
            raise ValueError(f"Invalid size. Must be one of: {Product.VALID_SIZES}")
        return size.lower()
    
    def get_item_id(self):
        return self._item_id
    
    def get_name(self):
        return self._name
    
    def get_price(self):
        return self._price
    
    def get_quantity(self):
        return self._quantity
    
    def get_size(self):
        return self._size
    
    def set_quantity(self, quantity):
        if quantity >= 0:
            self._quantity = quantity
        else:
            raise ValueError("Quantity cannot be negative")
    
    def __str__(self):
        return f"{self._name} (ID: {self._item_id}) - Size: {self._size}, Price: ${self._price:.2f}, Stock: {self._quantity}"
    
    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return self._item_id == other._item_id

class Furniture(Product):
    def get_product_type(self):
        return "Furniture"

class Electronics(Product):
    def get_product_type(self):
        return "Electronics"

class Clothing(Product):
    def get_product_type(self):
        return "Clothing"

class Accessories(Product):
    def get_product_type(self):
        return "Accessories"

class ItemCatalog:
    def __init__(self):
        self._items = {}
    
    def add_item(self, product):
        if product.get_item_id() not in self._items:
            self._items[product.get_item_id()] = product
            return True
        return False
    
    def get_item(self, item_id):
        return self._items.get(item_id)
    
    def get_all_items(self):
        return list(self._items.values())
    
    def update_stock(self, item_id, quantity):
        item = self.get_item(item_id)
        if item:
            item.set_quantity(item.get_quantity() - quantity)
            return True
        return False

def create_sample_catalog():
    catalog = ItemCatalog()
    catalog.add_item(Furniture(101, "Sofa", 499.99, 10, "extra-large"))
    catalog.add_item(Furniture(102, "Coffee Table", 149.99, 25, "large"))
    catalog.add_item(Electronics(201, "Laptop", 899.99, 15, "medium"))
    catalog.add_item(Electronics(202, "Smartphone", 699.99, 30, "small"))
    catalog.add_item(Clothing(301, "Winter Jacket", 129.99, 50, "large"))
    catalog.add_item(Accessories(401, "Backpack", 49.99, 100, "medium"))
    catalog.add_item(Electronics(203, "Headphone", 399.99, 0, "small"))
    catalog.add_item(Clothing(302, "Yogapants", 299.99, 1, "small"))
    return catalog