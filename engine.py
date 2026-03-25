#this is the main engine file for the mini trading engine. It will contain the main logic for the trading engine, including order matching, order book management, and trade execution.

class Order:
    def __init__(self, symbol, side, price, quantity):
        self.symbol = symbol
        self.side = side
        self.price = price
        self.quantity = quantity

        if self.price <= 0:
            raise ValueError("Price must be greater than zero")
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
    
#class OrderBook:
#logic to manage the order book for each symbol, including adding and removing orders, and matching orders

class Position: 
    def __init__(self, symbol, quantity, average_price):
        self.symbol = symbol
        self.quantity = quantity
        self.average_price = average_price

class Portfolio:

   
    @property #getter method to get the cash balance of the portfolio
    def cash(self):
        return self._cash 
    
    def __init__(self, cash):
        self.positions = {} #initialize positions for each symbol
        self._cash = cash #initial cash balance for the portfolio
    
    def __repr__(self):
        return f"Portfolio(cash={self._cash}, positions={self.positions})"
    
    def __str__(self):
        return f"Portfolio with cash: ${self._cash} and positions: {self.positions}"
    
    def __iter__(self):
        return iter(self.positions.values())
    def __getitem__(self, symbol):
        return self.positions.get(symbol, None)
    
    def execute_order(self, order):
        #execute the order and update the portfolio
        if order.side.upper() == 'BUY':
            self._buy(order)
        elif order.side.upper() == 'SELL':
            self._sell(order)

    def _buy(self, order):
        total_value = order.price * order.quantity

        if total_value > self._cash:
            raise Exception("Insufficient cash to execute the buy order")

        symbol = order.symbol
        # Case 1: First time buying this symbol
        if symbol not in self.positions:
            self.positions[symbol] = Position(symbol, order.quantity, order.price)
            self._cash -= total_value
            return
        # Case 2: Existing position → weighted average update
        pos = self.positions[symbol]

        old_qty = pos.quantity
        old_avg = pos.average_price

        new_qty = old_qty + order.quantity
        new_avg = ((old_qty * old_avg) + (order.quantity * order.price)) / new_qty

        pos.quantity = new_qty
        pos.average_price = new_avg

        # Update cash
        self._cash -= total_value          

    def _sell(self, order):

        symbol = order.symbol
        if symbol not in self.positions:
            raise Exception("No existing position to sell")

        pos = self.positions[symbol]

        if order.quantity > pos.quantity:
            raise Exception("Insufficient quantity to execute the sell order")

        total_value = order.price * order.quantity

        # Update position
        pos.quantity -= order.quantity

        # Update cash
        self._cash += total_value

        # If position is fully sold, remove it from the portfolio
        if pos.quantity == 0:
            del self.positions[symbol]
    
    def portfolio_value(self):
        total_value = self._cash
        print(f"Cash: ${self._cash}")
        for pos in self.positions.values():
            total_value += pos.quantity * pos.average_price
        print(f"Total Position Values: ${total_value - self._cash}")
        print(f"Total Portfolio Value: ${total_value}")

    def portfolio_view(self):
        for symbol, position in self.positions.items():
            print(f"Symbol: {symbol}, Quantity: {position.quantity}, Average Price: ${position.average_price}")

#create demo order 
order1 = Order('AAPL', 'BUY', 150, 100) #buy 100 shares of AAPL at $150
order2 = Order('GOOG', 'BUY', 180, 75) #buy 75 shares of GOOG at $180
order3 = Order('GOOG', 'SELL', 250, 50) #sell 50 shares of GOOG at $250
#initialize portfolio
portfolio = Portfolio(100000)
#execute orders
portfolio.execute_order(order1)
portfolio.execute_order(order2)
portfolio.execute_order(order3)

portfolio.portfolio_value()
portfolio.portfolio_view()

