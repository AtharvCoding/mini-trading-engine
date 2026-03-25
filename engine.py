class Order:
    def __init__(self, symbol, side, price, quantity):
        self.symbol = symbol
        self.side = side.upper()
        self.price = price
        self.quantity = quantity

        if self.price <= 0:
            raise ValueError("Price must be greater than zero")
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        if self.side not in ["BUY", "SELL"]:
            raise ValueError("Side must be BUY or SELL")


class Position:
    def __init__(self, symbol, quantity, average_price):
        self.symbol = symbol
        self.quantity = quantity
        self.average_price = average_price

    def buy(self, qty, price):
        new_qty = self.quantity + qty
        self.average_price = (
            (self.quantity * self.average_price + qty * price) / new_qty
        )
        self.quantity = new_qty

    def sell(self, qty):
        if qty > self.quantity:
            raise ValueError("Insufficient quantity to sell")
        self.quantity -= qty

    def value(self):
        return self.quantity * self.average_price

    def __repr__(self):
        return f"Position({self.symbol}, qty={self.quantity}, avg={self.average_price:.2f})"


class Portfolio:
    def __init__(self, initial_cash=1_000_000):
        self._cash = initial_cash
        self.positions = {}

    @property
    def cash(self):
        return self._cash

    def __repr__(self):
        return f"Portfolio(cash={self._cash:.2f}, positions={list(self.positions.values())})"

    def __iter__(self):
        return iter(self.positions.values())

    def __getitem__(self, symbol):
        return self.positions[symbol]  # raises KeyError if missing (correct behavior)

    def execute_order(self, order):
        if order.side == "BUY":
            self._buy(order)
        else:
            self._sell(order)

    def _buy(self, order):
        total_cost = order.price * order.quantity

        if total_cost > self._cash:
            raise ValueError("Insufficient cash")

        symbol = order.symbol

        if symbol not in self.positions:
            self.positions[symbol] = Position(symbol, order.quantity, order.price)
        else:
            self.positions[symbol].buy(order.quantity, order.price)

        self._cash -= total_cost

    def _sell(self, order):
        symbol = order.symbol

        if symbol not in self.positions:
            raise ValueError("No position to sell")

        pos = self.positions[symbol]
        pos.sell(order.quantity)

        self._cash += order.price * order.quantity

        if pos.quantity == 0:
            del self.positions[symbol]

    def position_values(self):
        return (p.value() for p in self.positions.values())  # generator

    def total_value(self):
        return self._cash + sum(self.position_values())