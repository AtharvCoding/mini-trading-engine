#this is the main engine file for the mini trading engine. It will contain the main logic for the trading engine, including order matching, order book management, and trade execution.

class Order:
    def __init__(self, symbol, side, price, quantity):
        self.symbol = symbol
        self.side = side
        self.price = price
        self.quantity = quantity
    
#class OrderBook:
#logic to manage the order book for each symbol, including adding and removing orders, and matching orders

class Position: 
    def __init__(self, symbol, quantity, average_price):
        self.symbol = symbol
        self.quantity = quantity
        self.average_price = average_price

class Portfolio:

    _cash= 1000000 #initial cash balance
    @property #getter method to get the cash balance of the portfolio
    def cash(self):
        return self._cash 
    
    def __init__(self):
        self.positions = {} #initialize positions for each symbol
    
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
        pass #logic to execute sell order and update position and cash balance


#create demo order 
order1 = Order('AAPL', 'BUY', 150, 100) #buy 100 shares of AAPL at $150
order2 = Order('GOOG', 'SELL', 2500, 50) #sell 50 shares of GOOG at $2500
#initialize portfolio
portfolio = Portfolio()
#execute orders
portfolio.execute_order(order1)
portfolio.execute_order(order2)