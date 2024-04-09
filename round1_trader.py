from datamodel import OrderDepth, TradingState, Order
from typing import List, Dict
from collections import deque
import pandas as pd

class Trader:
    def __init__(self) -> None:
        self.amethyst_buyprice = 9998
        self.amethyst_sellprice = 10002
        self.starfruit_prices = deque(maxlen=100)
        self.roc_buy = -5
        self.roc_sell = 5
    
    def calculate_roc(self, product: str, state: TradingState) -> float:
        # Retrieve price data for the product
        trades = state.market_trades.get(product, [])
        prices = [trade.price for trade in trades]
        self.starfruit_prices.extend(prices)
        print(self.starfruit_prices)

        # Ensure there are at least 100 data points
        if len(self.starfruit_prices) < 100:
            print("Not enough data points")
            return 0.0  # Return a default value for ROC

        # Calculate differences between consecutive prices
        price_diffs = []
        for i in range(1, len(self.starfruit_prices)):
            diff = self.starfruit_prices[i] - self.starfruit_prices[i - 1]
            price_diffs.append(diff)

        print(" price diffs " + str(price_diffs))
        
        # Calculate rolling sum of differences over the last 100 data points
        window_size = 100
        starfruit_diff_agg = sum(price_diffs[-window_size:])
        print(" diff agg " + str(starfruit_diff_agg))
        
        # Now you can use starfruit_diff_agg for further analysis or return it as needed
        return starfruit_diff_agg

    
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

                    if int(best_ask) <= self.amethyst_buyprice:
                        print("BUY", str(-best_ask_amount) + "x", best_ask)
                        orders.append(Order(product, best_ask, -best_ask_amount))

                if len(order_depth.sell_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())  # Get the highest bid price
                    best_bid_amount = order_depth.buy_orders[best_bid]

                    if int(best_bid) >= self.amethyst_sellprice:
                        print("SELL", str(best_bid_amount) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_amount))

            elif product == "STARFRUIT":
                # Starfruit strategy
                if len(order_depth.sell_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())  # Get the highest bid price
                    best_bid_amount = order_depth.buy_orders[best_bid]
                    
                    best_ask = min(order_depth.sell_orders.keys())  # Get the lowest ask price
                    best_ask_amount = order_depth.sell_orders[best_ask]

                    roc = self.calculate_roc(product, state)
                    print(str(roc))

                    if roc >= self.roc_sell:
                        # adjust sell for the amount can sell
                        print("SELL", str(best_bid_amount) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_amount))
                
                    if roc <= self.roc_buy:
                        print("BUY", str(-best_ask_amount) + "x", best_ask)
                        orders.append(Order(product, best_ask, -best_ask_amount))

            result[product] = orders
        
        trader_data = "SAMPLE"
        conversions = 1
        return result, conversions, trader_data