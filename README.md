<b>PROBLEM STATEMENT</b>


Design and implement a simplified portfolio management system using Python classes.
The goal is to simulate how a basic trading system processes orders, manages positions,
and tracks total portfolio value.

You must build three main components:

1. Order Class:
   - Represents a trade instruction.
   - Attributes:
       symbol (str), quantity (int), price (float), side ("BUY" or "SELL")
   - Validate all inputs (no negative values, valid side only).

2. Position Class:
   - Represents holdings for a single stock.
   - Attributes:
       symbol, quantity, average price
   - Must:
       - Update correctly on BUY (weighted average price)
       - Update correctly on SELL (reduce quantity)
       - Prevent selling more than available quantity
   - Provide a method to compute total value of the position.

3. Portfolio Class:
   - Represents the entire portfolio.
   - Attributes:
       cash (float), positions (dict mapping symbol → Position)
   - Must:
       - Execute orders via an `execute_order(order)` method
       - Handle BUY:
           - Check sufficient cash
           - Deduct cash
           - Update or create position
       - Handle SELL:
           - Check position exists
           - Check sufficient quantity
           - Add cash
           - Update position

Additional Requirements:
   - Implement a method to compute total portfolio value:
         total_value = cash + sum of all position values
   - Make Portfolio iterable (loop through positions)
   - Support indexing like: portfolio["AAPL"]
   - Implement a readable __repr__ for Portfolio
   - Use at least one @property
   - Use a generator or comprehension where appropriate
   - Handle all invalid cases using exceptions

Edge Cases to Handle:
   - Buying without enough cash
   - Selling a stock that does not exist
   - Selling more than owned quantity
   - Negative or zero inputs

Test your system with multiple buy/sell orders and verify:
   - Cash updates correctly
   - Positions update correctly
   - Total portfolio value is accurate

Goal:
Focus on clean design, proper use of classes, and correct data handling.

