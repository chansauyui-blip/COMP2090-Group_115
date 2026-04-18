from item import create_sample_catalog
from transport import TransportManager
from time_schedule import TimeSchedule

class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
        self.delivery_days = 0

    def get_subtotal(self):
        return self.product.get_price() * self.quantity

    def get_size(self):
        return self.product.get_size()

    def set_delivery_days(self, days):
        self.delivery_days = days

    def get_delivery_days(self):
        return self.delivery_days

    def __str__(self):
        return f"{self.quantity}x {self.product.get_name()} - ${self.get_subtotal():.2f}"

class PurchaseSystem:
    def __init__(self):
        self.catalog = create_sample_catalog()
        self.cart = []
        self.selected_transport = None
        self.ship_separately = False
        self.size_priority = ["small", "medium", "large", "extra-large"]

    def get_largest_size(self):
        if not self.cart:
            return None
        sizes = [item.get_size() for item in self.cart]
        largest = "small"
        for s in sizes:
            if self.size_priority.index(s) > self.size_priority.index(largest):
                largest = s
        return largest

    def has_multiple_sizes(self):
        sizes = {item.get_size() for item in self.cart}
        return len(sizes) > 1

    def add_to_cart(self, item_id, quantity):
        item = self.catalog.get_item(item_id)
        if not item:
            return False, "Item not found"

        if quantity <= 0:
            return False, "Quantity must be positive"

        if quantity > item.get_quantity():
            return False, f"Insufficient stock. Only {item.get_quantity()} available"

        for cart_item in self.cart:
            if cart_item.product == item:
                cart_item.quantity += quantity
                return True, "Item quantity updated in cart"

        self.cart.append(CartItem(item, quantity))
        return True, "Item added to cart"

    def remove_from_cart(self, item_id):
        for i, cart_item in enumerate(self.cart):
            if cart_item.product.get_item_id() == item_id:
                del self.cart[i]
                return True, "Item removed from cart"
        return False, "Item not in cart"

    def set_shipping_option(self, separate):
        self.ship_separately = separate
        self.calculate_all_delivery_days()

    def select_transport(self, plan_id):
        plan = TransportManager.get_plan_by_id(plan_id)
        if plan:
            self.selected_transport = plan
            self.calculate_all_delivery_days()
            return True, f"Selected {plan.get_name()} transport (applied to all items)"
        return False, "Invalid transport plan"

    def calculate_all_delivery_days(self):
        if not self.cart or not self.selected_transport:
            return

        largest_size = self.get_largest_size()
        largest_days = self.selected_transport.calculate_delivery_days(largest_size)

        for item in self.cart:
            if self.ship_separately:
                item_days = self.selected_transport.calculate_delivery_days(item.get_size())
                item.set_delivery_days(item_days)
            else:
                item.set_delivery_days(largest_days)

    def calculate_total(self):
        if not self.cart:
            return 0.0, 0.0, 0.0

        subtotal = sum(item.get_subtotal() for item in self.cart)
        transport_cost = self.selected_transport.calculate_price() if self.selected_transport else 0.0
        total = subtotal + transport_cost
        return subtotal, transport_cost, total

    def get_arrival_dates(self):
        if not self.cart or not self.selected_transport:
            return []

        dates = []
        seen_dates = set()
        for item in self.cart:
            date_str = TimeSchedule.calculate_arrival_date(item.get_delivery_days())
            entry = f"{item.product.get_name()}: {date_str}"
            if self.ship_separately:
                dates.append(entry)
            else:
                if date_str not in seen_dates:
                    dates.append(f"All items: {date_str}")
                    seen_dates.add(date_str)
        return dates

    def checkout(self):
        if not self.cart:
            return False, "Cart is empty"

        if not self.selected_transport:
            return False, "Please select a transport plan"

        for cart_item in self.cart:
            self.catalog.update_stock(cart_item.product.get_item_id(), cart_item.quantity)

        subtotal, transport_cost, total = self.calculate_total()
        arrival_dates = self.get_arrival_dates()

        order_summary = {
            "order_items": [str(item) for item in self.cart],
            "subtotal": subtotal,
            "transport": transport_cost,
            "total": total,
            "arrival_dates": arrival_dates,
            "transport_plan": self.selected_transport.get_name(),
            "shipping_option": "Separately" if self.ship_separately else "Together"
        }

        self.cart = []
        self.selected_transport = None
        self.ship_separately = False

        return True, order_summary

    def get_available_items(self):
        return self.catalog.get_all_items()

    def get_available_transports(self):
        return TransportManager.get_all_plans()

    def get_cart_items(self):
        return self.cart