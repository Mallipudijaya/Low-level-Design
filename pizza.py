from abc import ABC, abstractmethod

# Topping interface equivalent
class Topping(ABC):
    @abstractmethod
    def get_price(self):
        pass

    @abstractmethod
    def get_description(self):
        pass

# MushroomTopping class
class MushroomTopping(Topping):
    def __init__(self):
        self.price = 10

    def get_price(self):
        return self.price

    def get_description(self):
        return "Mushroom Topping"

# Size enum equivalent
class Size:
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

# Cheese enum equivalent
class Cheese:
    PEPPERONI = "Pepperoni"
    ITALIAN = "Italian"
    NORMAL = "Normal"

# Pizza class
class Pizza:
    def __init__(self):
        self.toppings = []
        self.size = None
        self.cheese = None
        self.total_price = 0.0

    def add_topping(self, topping):
        self.toppings.append(topping)

    def add_cheese(self, cheese):
        self.cheese = cheese

    def with_size(self, size):
        self.size = size

    def get_total_price(self):
        sum_price = sum([t.get_price() for t in self.toppings])
        return sum_price * self.size

# PizzaBuilder class
class PizzaBuilder:
    def __init__(self):
        self.pizza = Pizza()

    def add_topping(self, topping):
        self.pizza.add_topping(topping)
        return self

    def add_cheese(self, cheese):
        self.pizza.add_cheese(cheese)
        return self

    def with_size(self, size):
        self.pizza.with_size(size)
        return self

    def build(self):
        return self.pizza

# Main example
if __name__ == "__main__":
    p = PizzaBuilder().add_cheese(Cheese.ITALIAN) \
                      .add_topping(MushroomTopping()) \
                      .with_size(Size.MEDIUM) \
                      .build()
    print(f"I am building a pizza AND ITS price is: {p.get_total_price()}")
