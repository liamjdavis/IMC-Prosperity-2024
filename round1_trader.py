from datamodel import OrderDepth, TradingState, Order
from typing import List, Dict

class Trader:
    def __init__(self) -> None:
        self.amethyst_buyprice = 9998
        self.amethyst_sellprice = 10002
    
    def calculate_roc(self, product: str, state: TradingState) -> float:
        # Retrieve price data for the product
        price_data = state.observations.plainValueObservations.get(product, [])

        # Ensure there are at least 100 data points
        if len(price_data) < 100:
            return 0.0  # Return a default value for ROC

        # Calculate ROC for the last 100 data points
        roc_values = []
        for i in range(-100, 0):
            roc = ((price_data[i] - price_data[i + 1]) / price_data[i + 1]) * 100
            roc_values.append(roc)

        # Calculate and return the average ROC
        avg_roc = sum(roc_values) / len(roc_values)
        return avg_roc
    
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        result = {}

        for product, order_depth in state.order_depths.items():
            orders: List[Order] = []
            print(product)
            
            if product == "AMETHYSTS":
                print("Amethysts")
                # Amethyst strategy
                if len(order_depth.sell_orders) != 0:
                    best_ask = min(order_depth.sell_orders.keys())  # Get the lowest ask price
                    best_ask_amount = order_depth.sell_orders[best_ask]

                    if best_ask < self.amethyst_buyprice:
                        orders.append(Order(product, best_ask, -best_ask_amount))

                if len(order_depth.sell_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())  # Get the highest bid price
                    best_bid_amount = order_depth.buy_orders[best_bid]

                    if best_bid > self.amethyst_sellprice:
                        orders.append(Order(product, best_bid, -best_bid_amount))

            elif product == "STARFRUIT":
                # Starfruit strategy
                if len(order_depth.sell_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())  # Get the highest bid price
                    best_bid_amount = order_depth.buy_orders[best_bid]

                    roc = self.calculate_roc(product, state)
                    print(str(roc))

                    if roc > 10:
                        orders.append(Order(product, best_bid, -best_bid_amount))
                
                    if roc < -10:
                        orders.append(Order(product, best_bid, best_bid_amount))

            result[product] = orders
        
        trader_data = "SAMPLE"
        conversions = 1
        return result, conversions, trader_data