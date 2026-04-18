from abc import ABC, abstractmethod

class TransportPlan(ABC):
    SIZE_DAY_MULTIPLIER = {
        "small": 1,
        "medium": 1.5,
        "large": 2,
        "extra-large": 3
    }
    
    def __init__(self, plan_id, name, base_price, base_days):
        self._plan_id = plan_id
        self._name = name
        self._base_price = base_price
        self._base_days = base_days
    
    @abstractmethod
    def calculate_delivery_days(self, item_size):
        pass
    
    @abstractmethod
    def calculate_price(self):
        pass
    
    def get_plan_id(self):
        return self._plan_id
    
    def get_name(self):
        return self._name
    
    def get_base_price(self):
        return self._base_price
    
    def get_base_days(self):
        return self._base_days
    
    def __str__(self):
        return f"{self._name} Plan - Base Price: ${self._base_price:.2f}, Base Days: {self._base_days}"

class StandardPlan(TransportPlan):
    def __init__(self):
        super().__init__(1, "Standard", 9.99, 3)
    
    def calculate_delivery_days(self, item_size):
        return int(self._base_days * self.SIZE_DAY_MULTIPLIER[item_size])
    
    def calculate_price(self):
        return self._base_price

class ExpressPlan(TransportPlan):
    def __init__(self):
        super().__init__(2, "Express", 19.99, 1)
    
    def calculate_delivery_days(self, item_size):
        return int(self._base_days * self.SIZE_DAY_MULTIPLIER[item_size])
    
    def calculate_price(self):
        return self._base_price

class PremiumPlan(TransportPlan):
    def __init__(self):
        super().__init__(3, "Premium", 39.99, 0.5)
    
    def calculate_delivery_days(self, item_size):
        return max(1, int(self._base_days * self.SIZE_DAY_MULTIPLIER[item_size]))
    
    def calculate_price(self):
        return self._base_price

class TransportManager:
    _available_plans = [StandardPlan(), ExpressPlan(), PremiumPlan()]
    
    @classmethod
    def get_all_plans(cls):
        return cls._available_plans
    
    @classmethod
    def get_plan_by_id(cls, plan_id):
        for plan in cls._available_plans:
            if plan.get_plan_id() == plan_id:
                return plan
        return None